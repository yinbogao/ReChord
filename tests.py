"""tests.py contains a test for every back-end algorithm"""


from lxml import etree
from search import prepare_tree, find_artic, search, get_attrib_from_element, \
    get_mei_from_folder, get_title, get_creator, find_expressive_term, check_element_match, root_to_list, \
    text_box_search_folder, text_box_search, snippet_search_folder


def positive_test_find_expressive_term():
    """Positive test for find_expressive_term"""
    _, root = prepare_tree('database/test_files/Chopin.xml')
    element_et_list = find_expressive_term(root, 'legatissimo')
    assert len(element_et_list), "find_expressive_term: legatissimo not found."


def positive_test_find_artic():
    """Positive test for find_artic"""
    _, root = prepare_tree('database/test_files/Chopin.xml')
    element_artic_list = find_artic(root, 'stacc')
    assert len(element_artic_list) != 0, "find_artic: stacc not found"


def positive_test_search():
    """Positive test for search"""
    tree, _ = prepare_tree('database/test_files/Chopin.xml')
    input_xml = etree.parse('database/test_files/testinput.xml')
    input_root = input_xml.getroot()
    measure_match_list = search(input_root, tree)
    assert len(measure_match_list) != 0, "search: unsuccessful"


def positive_test_get_attrib_from_element():
    """Positive test for get_attrib_from_element"""
    tree, _ = prepare_tree('database/test_files/Chopin.xml')
    attrib_ls = get_attrib_from_element(tree, 'note', 'pname')
    assert len(attrib_ls) != 0, "positive_test_get_attrib_from_element: no attributes found"


def positive_test_get_mei_from_folder():
    """Positive test for get_mei_from_database"""
    all_mei_files = get_mei_from_folder('database/MEI_Complete_examples')
    assert len(all_mei_files) != 0, "get_mei_from_database: no files found"


def positive_test_get_title():
    """Positive test for get_title"""
    title_list = get_title('database/test_files/Chopin.xml')
    assert len(title_list) != 0, "get_title: title not found"


def positive_test_get_creator():
    """Positive test for get_creator"""
    creator_list = get_creator('database/test_files/Chopin.xml')
    assert len(creator_list) != 0, "get_creator: creator (composer) not found"


def positive_test_check_element_match():
    """positive test for seeing if all elements in a file match themselves"""
    _, root = prepare_tree('database/test_files/Chopin.xml')
    for element in root_to_list(root):
        assert check_element_match(element, element), \
            "check_element_match: element not equal to themselves; check Element with id " + element.attrib["xml:id"]


def positive_test_text_box_search_folder():
    """positive test for ensuring the text box search method appropriately searches through a full folder"""
    assert len(text_box_search_folder("database/MEI_Complete_examples", "Expressive Terms", "cresc.")) != 0, \
        "cannot find crescendo in folder"


def positive_test_text_box_search():
    """positive test to make sure text box search method completes a search through a given mei file"""
    _, root = prepare_tree('database/test_files/Chopin.xml')
    assert len(text_box_search(root, "Expressive Terms", "legatissimo")) != 0, "cannot find legatissimo expressive term"


def positive_test_snippet_search_folder():
    """positive test to see if the search method will traverse a folder and output matches between the
        snippet and the files in the folder"""
    input_xml = etree.parse('database/test_files/Aguado_Walzer_G-major_SNIPPET_TEST.xml')
    assert len(snippet_search_folder("database/MEI_Complete_examples", input_xml)) != 0, \
        "no matches found between input file and folder"


def main():
    """implements test methods"""
    positive_test_find_expressive_term()
    positive_test_find_artic()
    positive_test_search()
    positive_test_get_attrib_from_element()
    positive_test_get_mei_from_folder()
    positive_test_get_title()
    positive_test_get_creator()
    positive_test_check_element_match()
    positive_test_text_box_search_folder()
    positive_test_text_box_search()
    positive_test_snippet_search_folder()


if __name__ == '__main__':
    main()
