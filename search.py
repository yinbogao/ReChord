from lxml import etree
import os

namespace = '{http://www.music-encoding.org/ns/mei}'

# Generic Functions


def string_to_root(string_in):
    """
    Arguments: string_in [string]: input in XML format in a string
    Return: [element]: root element of parsed etree
    """

    return etree.fromstring(string_in)


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
    Arguments: root [element] : root element to be converted to list
    Returns: [list] List of element objects in depth-first order
    """

    return list(root.iter())


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
    return tree.xpath(
        "//mei:" + tag,
        namespaces={'mei': 'http://www.music-encoding.org/ns/mei'}
    )


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
    arr = first.getchildren()
    title_list = [element for element in arr if element.tag == "{http://www.music-encoding.org/ns/mei}title"]
    return title_list


def get_creator(tree):
    """return a list of all composers (creators) in the piece
    Arguments: tree [etree]: tree of mei file
    Return: creators_list [List<element>]: List of elements marking the creator(s) of a piece
    """
    children = get_elements(tree, 'respStmt')[0].getchildren()
    creators_list = [element for element in children if element.attrib['role'] == "creator"]
    return creators_list


def find_expressive_term(root, expressive_term):
    """return a list of elements that has expressive term that is of expressive_term
    Arguments: tree [etree]: tree to be searched
               expressive_term [string]: expressive term to be found
    Return: all_et_list [List<int>]: list of measure numbers of elements with given expressive term
    """
    music = root.find("{http://www.music-encoding.org/ns/mei}music")
    et_test = music.iter("{http://www.music-encoding.org/ns/mei}dir")
    return [get_measure(element) for element in et_test if element.text == expressive_term]


def find_artic(tree, artic_name):
    """parse a tree to a list of elements that has articulations that is of artic_name
    Arguments: tree [etree]: tree to be search
               artic_name [string]: articulation to be searched
    Return: element_artic_list [List<element>]: list of elements with given articulation
    """
    music = tree.getroot.find("{http://www.music-encoding.org/ns/mei}music")
    all_artic_list = music.iter("{http://www.music-encoding.org/ns/mei}artic")
    return [element for element in all_artic_list if element.attrib['artic'] == artic_name]


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

    return [filename for filename in os.listdir(path) if filename.endswith('.mei')]


def check_element_match(element1, element2):
    """checks whether element1 and element2 match by our definitions

    Arguments: element1 and element2 are both lxml Element type
    Returns: ([boolean]) true if they match all given parameters for tag type, false else

    """

    if element1.tag == element2.tag:
        tag = element1.tag

        if tag == namespace + "note":
            # check pname and dur of note

            if element1.attrib["pname"] != element2.attrib["pname"]:
                return False

            if 'dur' in element1.attrib and 'dur' in element2.attrib:
                if element1.attrib["dur"] != element2.attrib["dur"]:
                    return False

            if 'oct' in element1.attrib and 'oct' in element2.attrib:
                if element1.attrib["oct"] != element2.attrib["oct"]:
                    return False

            if 'stem.dir' in element1.attrib and 'stem.dir' in element2.attrib:
                if element1.attrib["stem.dir"] != element2.attrib["stem.dir"]:
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

