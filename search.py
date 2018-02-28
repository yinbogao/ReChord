from lxml import etree

namespace = '{http://www.music-encoding.org/ns/mei}'

# Generic Functions

def prepare_tree(xml_file):
    """create etree and root from the given xml file"""
    tree = etree.parse(xml_file)
    root = tree.getroot()
    return tree, root


def tree_to_list(root):
    ret_list=[]
    for element in root.iter():
        ret_list.append(element)
    return ret_list


def get_measure(element):
    while element.tag != '{http://www.music-encoding.org/ns/mei}measure':
        element = element.getparent()
    return element.attrib['n']


def get_elements(tree, tag):
    """return list of all elements of the tag from tree"""
    search_term = "//mei:" + tag
    r = tree.xpath(search_term,
                   namespaces={'mei': 'http://www.music-encoding.org/ns/mei'})
    return r


def get_elements_has_attrib(tree, tag, att_name):
    """return a list of element that is of the tag and contain the attrib"""
    elements_list = get_elements(tree, tag)
    filtered_element_list = [element for element in elements_list if element.attrib[att_name]]
    return filtered_element_list


def get_attrib_from_element(tree, tag, att_name):
    """return a list of element that is of the tag and contain the attrib"""
    elements_list = get_elements(tree, tag)
    attrib_list = [element.attrib[att_name] for element in elements_list if element.attrib[att_name]]
    return attrib_list


# Specific Functions


def find_artic(tree, artic_name):
    """return a list of elements that has articulations that is of artic_name"""
    all_artic_list = get_elements(tree, 'artic')
    element_artic_list = [element for element in all_artic_list if element.attrib['artic'] == artic_name]
    return element_artic_list


def notes_on_beam(tree):
    """return a list of nested list where each nested list is the notes on a beam"""

    # get a list of all the beam elements
    r = get_elements(tree, 'beam')
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


def search(input_root, data_tree):
    """input_root is a root of elements to be searched for
       data_tree is an etree to be searched"""
    #todo: fix variable names to stop using camelcase
    #todo: either fix firstEltMatch or eliminate
    #todo: work on how staffs are split
    #todo: issues with things like measures and dividers between notes
    counter = 0
    firstEltMatch = None
    inputList = []
    for element in input_root.iter():
        inputList.append(element)
        element.tag = "{http://www.music-encoding.org/ns/mei}" + element.tag
    measure_match_list = []
    for element in data_tree.getroot().iter():
        # elTag = str(element.tag)
        if (counter == len(inputList) - 1):
            measure_match_list.append(get_measure(element))
            # todo: currently returns measure of last element in search param, should be first
            counter = 1

        if element.tag == (inputList[counter].tag):

            if element.tag == namespace + 'note':
                if element.attrib['pname'] == inputList[counter].attrib['pname']:

                    if counter == 1: firstEltMatch = get_measure(element)
                    counter += 1

            elif element.tag == namespace + 'rest':

                if counter == 1:
                    firstEltMatch = get_measure(element)
                counter += 1

            elif element.tag == namespace + 'artic':
                if (element.attrib['artic'] == inputList.attrib['artic']):

                    if counter == 1:
                        firstEltMatch = get_measure(element)
                    counter += 1

            else:
                if counter == 0: firstEltMatch = get_measure(element)
                counter += 1
        else:
            counter = 1
            firstEltMatch = -1
    return measure_match_list


def main():
    # prepare the tree for the file
    tree, root = prepare_tree('database/Chopin.xml')
    inputXML = etree.parse('testinput.xml')
    input_root = inputXML.getroot()

    #print a list of matches to testinput.XML from Chopin.XML
    print(search(input_root, tree))

    # get a list of all notes from the file
    attrib_ls = get_attrib_from_element(tree, 'note', 'pname')

    # get a list of artic elements
    element_ls = get_elements_has_attrib(tree, 'artic', 'artic')

    #print("-" * 10, "a list of artic elements' attributions dictionary", "-" * 10)
    #for element in element_ls:
        #print(element.attrib)

    # get a list of artic element that has a staccato articulation
    element_artic_list = find_artic(tree, 'stacc')
    #print("-" * 10, "artic elements that has a staccato articulation", "-" * 10)
    for element in element_artic_list:
        #print(get_measure(element))
        print("stacc is in measure:", get_measure(element))

    # print tests result
    #print("-" * 10, "all notes from the file", "-" * 10)
    #print(attrib_ls)



if __name__ == "__main__":
    main()
