from lxml import etree

tree = etree.parse("chopin.xml")
root = tree.getroot()
namespace = '{http://www.music-encoding.org/ns/mei}'
note_namespace = 'http://www.w3.org/XML/1998/namespace'
inputXML = etree.parse('testinput.xml')
inputRoot = inputXML.getroot()
def trial():
    r = tree.xpath('//mei:measure[@xml:id]',
                   namespaces = {'mei': namespace})

    tree.getpath(r[0])
    r[0].getparent()
    return r


def search(inputroot, dataTree):
    """inputList is a list of elements to be searched for
       dataTree is an etree to be searched"""

    counter = 0
    firstEltMatch = None
    inputList = []
    for element in inputroot.iter():
        inputList.append(element)
        element.tag = "{http://www.music-encoding.org/ns/mei}"+element.tag
    measureMatchList = []
    for element in dataTree.getroot().iter():
        #elTag = str(element.tag)
        if(counter==len(inputList)-1):
            measureMatchList.append(get_measure(element))
            #todo: currently returns measure of last element in search param, should be first
            counter = 1

        if element.tag==(inputList[counter].tag):

            if element.tag == namespace+'note' :
                if(element.attrib['pname']==inputList[counter].attrib['pname']):

                    if counter==1: firstEltMatch=get_measure(element)
                    counter += 1

            elif element.tag == namespace+'rest' :

                if counter == 1:
                    firstEltMatch = get_measure(element)
                counter += 1

            elif element.tag == namespace+'artic':
                if(element.attrib['artic']==inputList.attrib['artic']):

                    if counter == 1:
                        firstEltMatch=get_measure(element)
                    counter += 1

            else:
                if counter ==0: firstEltMatch = get_measure(element)
                counter += 1
        else:
            counter = 1
            firstEltMatch = -1
    return measureMatchList


def get_measure(element):
    if element == None :
        return -1
    while element.tag != '{http://www.music-encoding.org/ns/mei}measure':
        element = element.getparent()
    return element.attrib['n']


def get_elements(elementType, tree):
    """return list of all elements of type elementType from tree"""

    searchParam = "//mei:"+elementType
    r=tree.xpath(searchParam, namespaces = {'mei': 'http://www.music-encoding.org/ns/mei'})
    return r

def find_articulation(articName, tree):
    allArticList = get_elements('artic', tree)
    articList = []
    for articulation in allArticList:
        if(articulation.attrib['artic'] == articName):
            articList.append(articulation)
    return articList

def get_notes(tree):
    """return all the notes from the tree """

    # select all the note elements
    r = tree.xpath('//mei:note',
                   namespaces = {'mei': 'http://www.music-encoding.org/ns/mei'})

    # loop through r to get attrib dictionary, and select 'pname' key's value add to the list
    return [note.attrib['pname'] for note in r]

def notes_on_beam(tree):
    """return a list of nested list where each nested list is the notes on a beam"""

    # get a list of all the beam elements
    r = tree.xpath('//mei:beam',
                   namespaces={'mei': 'http://www.music-encoding.org/ns/mei'})
    beam_notes_list = []

    # loop through beam list
    for beam in r:

        # get the children of each beam
        children = beam.getchildren()

        # loop through the children of hte beam
        # todo: there might be artic ignored here
        ls = []
        for child in children:

            # if the child is a note, directly add to the list
            if child.tag == '{http://www.music-encoding.org/ns/mei}note':
                ls += child.attrib['pname']

            # else if the child is a rest, add "0" to the list
            elif child.tag == '{http://www.music-encoding.org/ns/mei}rest':
                ls += '0'

            # else if the child is a chord, add a list of notes to the list
            elif child.tag == '{http://www.music-encoding.org/ns/mei}chord':
                notes = child.getchildren()
                ls.append([note.attrib['pname'] for note in notes if note.tag == '{http://www.music-encoding.org/ns/mei}note'])
        beam_notes_list.append(ls)

    return beam_notes_list


print(search(inputRoot, tree))

#for n in inputRoot.iter():
#    print(n.tag)