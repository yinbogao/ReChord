from lxml import etree


# Generic Functions

def prepare_tree(xml_file):
    """create etree and root from the given xml file"""
    tree = etree.parse(xml_file)
    root = tree.getroot()
    return tree, root


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


def main():
    # prepare the tree for the file
    tree, root = prepare_tree('database/Chopin.xml')

    # get a list of all notes from the file
    attrib_ls = get_attrib_from_element(tree, 'note', 'pname')

    # get a list of artic elements
    element_ls = get_elements_has_attrib(tree, 'artic', 'artic')

    print("-" * 10, "a list of artic elements' attributions dictionary", "-" * 10)
    for element in element_ls:
        print(element.attrib)

    # get a list of artic element that has a staccato articulation
    element_artic_list = find_artic(tree, 'stacc')
    print("-" * 10, "artic elements that has a staccato articulation", "-" * 10)
    for element in element_artic_list:
        print(element)
        print("is in measure:", get_measure(element))

    # print tests result
    print("-" * 10, "all notes from the file", "-" * 10)
    print(attrib_ls)



if __name__ == "__main__":
    main()
