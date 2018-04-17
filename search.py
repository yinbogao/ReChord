"""search.py contains all back-end search algorithms"""


import os
from lxml import etree

namespace = '{http://www.music-encoding.org/ns/mei}'

# Generic Functions


def prepare_terms_dict():
    """
    return a dictionary of terms for searching through abbreviation
    Return: [dictionary]: key: term name (regular spelling); value: term abbreviation
    """

    with open('database/terms_dictionary.txt') as file_descriptor:
        text = file_descriptor.read()
    return {
        line.split('\t')[0]: line.split('\t')[2].strip('()')
        for line in text.splitlines()
        if len(line) == 5
        }


def string_to_root(string_in):
    """Arguments: string_in [string]: input in XML format in a string
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
    while element is not None and element.tag != '{http://www.music-encoding.org/ns/mei}measure':
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


def get_title(path):
    """"return a list of each line of the title of the piece
    Arguments: tree [etree]: tree of file to search
    Return: title_list [List<element>]: list of title elements
    """
    tree, _ = prepare_tree(path)
    title_stmt = get_elements(tree, 'titleStmt')
    first = title_stmt[0]
    arr = first.getchildren()
    title_list = [element.text for element in arr if element.tag == "{http://www.music-encoding.org/ns/mei}title"]
    return title_list


def get_creator(path):
    """return a list of all composers (creators) in the piece
    Arguments: tree [etree]: tree of mei file
    Return: creators_list [List<element>]: List of elements marking the creator(s) of a piece
    """
    tree, _ = prepare_tree(path)
    children = get_elements(tree, 'respStmt')[0].getchildren()
    creators_list = [element.text for element in children if element.attrib['role'] == "creator"]
    return creators_list


def find_expressive_term(root, expressive_term):
    """return a list of elements that has expressive term that is of expressive_term
    Arguments: root [xml Element]: root of the tree to be searched
               expressive_term [string]: expressive term to be found
    Return: all_et_list [List<int>]: list of measure numbers of elements with given expressive term
    """
    music = root.find("{http://www.music-encoding.org/ns/mei}music")
    et_test = music.iter("{http://www.music-encoding.org/ns/mei}dir")
    return [get_measure(element) for element in et_test if element.text == expressive_term]


def find_artic(root, artic_name):
    """parse a tree to a list of elements that has articulations that is of artic_name
    Arguments: root [xml Element]: root of the tree to be searched
               artic_name [string]: articulation to be searched
    Return: element_artic_list [List<int>]: list of elements with given articulation
    """

    music = root.find("{http://www.music-encoding.org/ns/mei}music")
    all_artic_list = music.iter("{http://www.music-encoding.org/ns/mei}artic")
    return [get_measure(element) for element in all_artic_list if element.attrib['artic'] == artic_name]


def find_dynam(root, dynam_name):
    """parse a tree to a list of elements that has dynamic marking that is of dynam_name
       Arguments: root [xml Element]: root of the tree to be searched
                  dynam_name [string]: dynamic term to be searched
       Return: et_list [List<int>]: list of elements with given articulation
       """
    music = root.find("{http://www.music-encoding.org/ns/mei}music")
    et_test = music.iter("{http://www.music-encoding.org/ns/mei}dynam")
    return [get_measure(element) for element in et_test if element.text == dynam_name]


def find_tempo(root, tempo):
    """parses an element tree for a specified tempo marking
       Arguments: root [xml Element]: root of tree to be searched
                  tempo [string]: tempo marking to be searched
       Return: et_test[list<int>]: list of measure numbers where tempo marking appears
    """
    music = root.find("{http://www.music-encoding.org/ns/mei}music")
    et_test = music.iter("{http://www.music-encoding.org/ns/mei}tempo")
    return [get_measure(element) for element in et_test if element.text == tempo]


def find_pedal_marking(root, marking):
    """parses an element tree for a specified pedal marking
       Arguments: root [xml Element]: root of tree to be searched
                  marking [string]: pedal marking to be searched
       Return: et_test[list<int>]: list of measure numbers where pedal marking appears
    """
    music = root.find("{http://www.music-encoding.org/ns/mei}music")
    et_test = music.iter("{http://www.music-encoding.org/ns/mei}pedal")
    return [get_measure(element) for element in et_test if element.attrib['dir'] == marking]


def notes_on_beam(tree):
    """return a list of nested list where each nested list is the notes on a beam for all beams in tree
    Arguments: tree [etree]: tree to be searched
    Return: beam_notes_list: [List<Element tag='beam'>] nested list of beam elements
    """

    # get a list of all the beam elements
    beam_list = get_elements(tree, 'beam')
    beam_notes_list = []

    # loop through beam list
    for beam in beam_list:

        # get the children of each beam
        children = beam.getchildren()

        # loop through the children of the beam
        # todo: there might be artic ignored here
        beam_children = []
        for child in children:

            # if the child is a note, directly add to the list
            if child.tag == '{http://www.music-encoding.org/ns/mei}note':
                beam_children += child.attrib['pname']

            # else if the child is a rest, add "0" to the list
            elif child.tag == '{http://www.music-encoding.org/ns/mei}rest':
                beam_children += '0'

            # else if the child is a chord, add a list of notes to the list
            elif child.tag == '{http://www.music-encoding.org/ns/mei}chord':
                notes = child.getchildren()
                beam_children.append([note.attrib['pname'] for note in notes if note.tag ==
                                      '{http://www.music-encoding.org/ns/mei}note'])
        beam_notes_list.append(beam_children)

    return beam_notes_list


def text_box_search(root, tag, search_term):
    """searches an mei file for an element which matches the tag and search term given
       Arguments: root [Element]: root element of tree to be searched
                  tag [string]: element type
                  search_term[string]: search term to find element
       Return: [list<int>]: List of measures where tag appears"""
    if tag == "Expressive Terms":
        return find_expressive_term(root, search_term)
    elif tag == "Articulation":
        return find_artic(root, search_term)
    elif tag == "Dynamic Markings":
        return find_dynam(root, search_term)
    elif tag == "Hairpin":
        return []
    elif tag == "Tempo Marking":
        return find_tempo(root, search_term)
    elif tag == "Piano Fingerings":
        return []
    elif tag == "Pedal Marking":
        return find_pedal_marking(root, search_term)
    else:
        return []


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
    else:
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


def get_mei_from_folder(path):
    """gets a list of MEI files from a given folder path
    Arguments: path [string]: absolute or relative path to folder
    Returns: all_mei_files: List<file>: list of mei files in path
    """
    return [path + "/" + filename for filename in os.listdir(path) if filename.endswith('.mei') or filename.endswith('.xml')]


def text_box_search_folder(path, tag, search_term):
    """applies the text_box_search() method to a full folder
    Arguments:  path [string]: absolute of relative path to folder
                tag [string]: element type
                search_term[string]: search term to find element
    Returns:    text_box_array [List<string>]: list of the path of the file that contains the given tag and the measure
                                                in which it is found
    """
    file_list = get_mei_from_folder(path)
    print(file_list)
    text_box_array = []
    for file in file_list:
        _, root = prepare_tree(file)
        tb_search_output_array = text_box_search(root, tag, search_term)
        string_list = []
        for element in tb_search_output_array:
            string_list.append(' '.join(str(e) for e in get_title(file)) + " by " +
                               ' '.join(str(e) for e in get_creator(file)) + element)
            text_box_array.append(string_list)
    return text_box_array



def snippet_search_folder(path, tree):
    """applies the search() method to a full folder
    Arguments:  path [string]: absolute of relative path to folder
                tree is an etree to be searched
    Returns:    regular_search_array[List<string>]: title, creator (composer) and
                    measure number in which the snippet is found
    """
    input_root = tree.getroot()
    file_list = get_mei_from_folder(path)
    result_list = {}

    for file in file_list:
        tree, _ = prepare_tree(file)
        search_output_array = search(input_root, tree)
        for element in search_output_array:
            key = str(' '.join(str(e) for e in get_title(file)) + " by " +
                               ' '.join(str(e) for e in get_creator(file)) + '\n' + " Measure Number: ")
            if key in result_list:
                result_list[key] = str (result_list[key] + "," + (element))
            else:
                result_list[key] = element

    return result_list
