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


def root_to_list(root):
    arr = []
    for element in root.iter():
        arr.append(element)
    return arr

def search(input_root, data_tree):
    """input_root is a root of elements to be searched for
       data_tree is an etree to be searched"""
    #todo: fix variable names to stop using camelcase
    #todo: either fix firstEltMatch or eliminate
    #todo: work on how staffs are split
    #todo: issues with things like measures and dividers between notes

    counter = 0
    input_list = root_to_list(input_root)
    data_list = root_to_list(data_tree.getroot())
    measure_match_list = []

    for i in range(len(data_list)-len(input_list)):
        for j in range(1, len(input_list)):
            match = False
            if(data_list[i+j].tag==input_list[j].tag):
                print("tagMatch")
                tag = data_list[i+j].tag
                if tag==namespace+"note":
                    if data_list[i+j].attrib["pname"]==input_list[j].attrib["pname"] and data_list[i+j].attrib["dur"]==input_list[j].attrib["dur"]:
                        match = True
                elif tag == namespace+"rest":
                    if data_list[i+j].attrib["dur"]==input_list[j].attrib["dur"]:
                        match = True
                elif tag == namespace+"artic":
                    if data_list[i+j].attrib["artic"]==input_list[j].attrib["artic"]:
                        match = True
                else:
                    match = True
                if j == len(input_list)-1:
                    measure_match_list.append(get_measure(data_list[i]))

            if(not match):
                break

    return measure_match_list


def tests():
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
    for element in input_root.iter():
        print(element.tag)
    # print tests result
    #print("-" * 10, "all notes from the file", "-" * 10)
    #print(attrib_ls)


def main():
    tests()


if __name__ == "__main__":
    main()
