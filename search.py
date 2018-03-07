from lxml import etree
import os

namespace = '{http://www.music-encoding.org/ns/mei}'

# Generic Functions


def prepare_tree(xml_file_path):
    """create etree and root from the given xml file
    Arguments: xml_file_path [string]: string of absolute or relative file URL
    Return: tree [etree]: etree of XML file element objects
            root [element] root element of tree
    """
    tree = etree.parse(xml_file_path)
    root = tree.getroot()
    return tree, root


def root_to_list(root):
    """takes in etree root node, parses it to a depth-first ordered list
    Arguments: root
    Returns: List of element objects in depth-first order
    """
    ret_list = []
    for element in root.iter():
        ret_list.append(element)
    return ret_list


def get_measure(element):
    """gets measure of an element
    Arguments: element [Element]: element you want to find the measure of
    Return: Measure Number [int]: measure number found in measure's attribute
    """
    while element.tag != '{http://www.music-encoding.org/ns/mei}measure':
        element = element.getparent()
    return element.attrib['n']


def get_elements(tree, tag):
    """return list of all elements of the tag from tree
    Arguments: tree [etree]: tree to search
               tag [string]: tag to search (without namespace)
    Return: List of elements of type tag
    """
    search_term = "//mei:" + tag
    r = tree.xpath(search_term,
                   namespaces={'mei': 'http://www.music-encoding.org/ns/mei'})
    return r


def get_elements_has_attrib(tree, tag, att_name):
    """return a list of element that is of the tag and contain the attrib
    Arguments: tree [etree]: tree to search
               tag [string]: element type to filter by (without namespace)
               att_name [string]: attribute you want to filter by
    Return: list of elements of type tag with attribute att_name
    """
    elements_list = get_elements(tree, tag)
    filtered_element_list = [element for element in elements_list if element.attrib[att_name]]
    return filtered_element_list


def get_attrib_from_element(tree, tag, att_name):
    """return a list of element that is of the tag and contain the attrib
    Argument: tree [etree]: tree to search
              tag [string]: element tag to search
              att_name [string]: attribute type of element to find
    Return: attrib_list [List<string>]: List of attributes of type att_type on elements of type tag
    """
    elements_list = get_elements(tree, tag)
    attrib_list = [element.attrib[att_name] for element in elements_list if element.attrib[att_name]]
    return attrib_list


# Specific Functions


def get_title(tree):
    """"return a list of each line of the title of the piece
    Arguments: tree [etree]: tree of file to search
    Return: title_list [List<element>]: list of title elements
    """
    title_stmt = get_elements(tree, 'titleStmt')
    first = title_stmt[0]
    print(first)
    arr = first.getchildren()
    title_list = [element for element in arr if element.tag == "{http://www.music-encoding.org/ns/mei}title"]
    # print(title_list)
    return title_list


def get_creator(tree):
    """return a list of all composers (creators) in the piece
    Arguments: tree [etree]: tree of mei file
    Return: creators_list [List<element>]: List of elements marking the creator(s) of a piece
    """
    resp_stmt = get_elements(tree, 'respStmt')
    first = resp_stmt[0]
    arr = first.getchildren()
    creators_list = [element for element in arr if element.attrib['role'] == "creator"]
    return creators_list


def find_expressive_term(tree, expressive_term):
    """return a list of elements that has expressive term that is of expressive_term
    Arguments: tree [etree]: tree to be searched
               expressive_term [string]: expressive term to be found
    Return: all_et_list [List<element>]: list of elements with given expressive term
    """
    all_et_list = get_elements(tree, 'dir')
    element_et_list = [element for element in all_et_list if element.text == expressive_term]
    return element_et_list


def find_artic(tree, artic_name):
    """parse a tree to a list of elements that has articulations that is of artic_name
    Arguments: tree [etree]: tree to be search
               artic_name [string]: articulation to be searched
    Return: element_artic_list [List<element>]: list of elements with given articulation
    """
    all_artic_list = get_elements(tree, 'artic')
    element_artic_list = [element for element in all_artic_list if element.attrib['artic'] == artic_name]
    return element_artic_list


def notes_on_beam(tree):
    """return a list of nested list where each nested list is the notes on a beam for all beams in tree
    Arguments: tree [etree]: tree to be searched
    Return: beam_notes_list: [List<Element tag='beam'>] nested list of beam elements
    """

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
                ls.append([note.attrib['pname'] for note in notes if note.tag ==
                           '{http://www.music-encoding.org/ns/mei}note'])
        beam_notes_list.append(ls)

    return beam_notes_list


def get_mei_from_database(path):
    """gets a list of MEI files from a given folder path
    Arguments: path [string]: absolute or relative path to folder
    Returns: all_mei_files: List<file>: list of mei files in path
    """
    all_mei_files = []
    for file in os.listdir(path):
        if file.endswith('.mei'):
            all_mei_files.append(file)
    return all_mei_files


def check_element_match(element1, element2):
    """checks whether element1 and element2 match by our definitions

    Arguments: element1 and element2 are both lxml Element type
    Returns: ([boolean]) true if they match all given parameters for tag type, false else

    """
    # todo: implement ability to decide which attributes to check on a search-by-search basis

    if element1.tag == element2.tag:
        tag = element1.tag

        if tag == namespace + "note":
            # check pname and dur of note

            if element1.attrib["pname"] == element2.attrib["pname"] :
                if 'dur' in element1.attrib and 'dur' in element2.attrib:
                    if element1.attrib["dur"] == element2.attrib["dur"]:
                        return True
                    return False
                return True

        elif tag == namespace + "rest":
            # check dur of rest
            if element1.attrib["dur"] == element2.attrib["dur"]:
                return True

        elif tag == namespace + "artic":
            # check name of articulation
            if element1.attrib["artic"] == element2.attrib["artic"]:
                return True

        else:
            # element isn't a note, rest, or articulation--don't need to check attributes
            return True
    return False


def search(input_root, data_tree):
    """Searches input_root for pattern in data_tree
    Arguments: input_root is a root of elements to be searched for
               data_tree is an etree to be searched
    Return: measure_match_list [List<int>]: list of measures where pattern appears (with repeats)
    """
    # todo: work on how staffs are split
    # todo: issues with things like measures and dividers between notes

    input_list = root_to_list(input_root)
    data_list = root_to_list(data_tree.getroot())
    measure_match_list = []

    # iterate over data MEI file
    for i in range(len(data_list)-len(input_list)):

        # iterate over input and check if each element matches
        for j in range(1, len(input_list)):

            if check_element_match(data_list[i+j], input_list[j]):
                # if last element in input_list, add measure to list of matches
                if j == len(input_list) - 1:
                    measure_match_list.append(get_measure(data_list[i]))

            else:
                # elements don't match->stop input iteration and move to next data element
                break

    return measure_match_list


def tests():
    # prepare the tree for the file
    tree, root = prepare_tree('database/Chopin.xml')
    inputXML = etree.parse('testinput.xml')
    input_root = inputXML.getroot()

    # print a list of matches to testinput.XML from Chopin.XML
    print(search(input_root, tree))

    # get a list of all notes from the file
    attrib_ls = get_attrib_from_element(tree, 'note', 'pname')

    # get a list of artic elements
    element_ls = get_elements_has_attrib(tree, 'artic', 'artic')

    # print("-" * 10, "a list of artic elements' attributions dictionary", "-" * 10)
    # for element in element_ls:
        # print(element.attrib)

    # get a list of artic element that has a staccato articulation
    element_artic_list = find_artic(tree, 'stacc')
    # print("-" * 10, "artic elements that has a staccato articulation", "-" * 10)
    for element in element_artic_list:
        # print(get_measure(element))
        print("stacc is in measure:", get_measure(element))
    for element in input_root.iter():
        print(element.tag)
    # print tests result
    # print("-" * 10, "all notes from the file", "-" * 10)
    # print(attrib_ls)

    # prints all expressive terms that match 'legatissimo' in the Chopin work
    element_et_list = find_expressive_term(tree, 'legatissimo')
    if len(element_et_list) != 0:
        for element in element_et_list:
            print(element.text + " in measure " + get_measure(element))
    else:
        print("Expressive term not found")

    # # prints all MEI files in database\MEI_Complete_examples
    # all_mei_files = get_mei_from_database('database\MEI_Complete_examples')
    # for element in all_mei_files:
    #     print(element)

    # finds title
    title_list = get_title(tree)
    for element in title_list:
        print(element.text)

    # finds composer (creator)
    print("by:")
    creators_list = get_creator(tree)
    for element in creators_list:
        print(element.text)


def main():
    tests()


if __name__ == "__main__":
    main()
