from search import prepare_tree, find_expressive_term, find_artic, search, get_attrib_from_element, \
    get_mei_from_database, get_title, get_creator
from lxml import etree
from search import prepare_tree, find_expressive_term, get_measure, check_element_match, tree_to_list


def positive_test_find_expressive_term():
    """Positive test for find_expressive_term"""
    _, root = prepare_tree('database/Chopin.xml')
    element_et_list = find_expressive_term(root, 'legatissimo')
    assert len(element_et_list) != 0, "find_expressive_term: legatissimo not found."


def positive_test_find_artic():
    """Positive test for find_artic"""
    _, root = prepare_tree('database/Chopin.xml')
    element_artic_list = find_artic(root, 'stacc')
    assert len(element_artic_list) != 0, "find_artic: stacc not found"


def positive_test_search():
    """Positive test for search"""
    tree, _ = prepare_tree('database/Chopin.xml')
    inputXML = etree.parse('testinput.xml')
    input_root = inputXML.getroot()
    measure_match_list = search(input_root, tree)
    assert len(measure_match_list) != 0, "search: unsuccessful"


def positive_test_get_attrib_from_element():
    """Positive test for get_attrib_from_element"""
    tree, _ = prepare_tree('database/Chopin.xml')
    attrib_ls = get_attrib_from_element(tree, 'note', 'pname')
    assert len(attrib_ls) != 0, "positive_test_get_attrib_from_element: no attributes found"


def positive_test_get_mei_from_database():
    """Positive test for get_mei_from_database"""
    all_mei_files = get_mei_from_database('database/MEI_Complete_examples')
    assert len(all_mei_files) != 0, "get_mei_from_database: no files found"


def positive_test_get_title():
    """Positive test for get_title"""
    tree, _ = prepare_tree('database/Chopin.xml')
    title_list = get_title(tree)
    assert len(title_list) != 0, "get_title: title not found"


def positive_test_get_creator():
    """Positive test for get_creator"""
    tree, _ = prepare_tree('database/Chopin.xml')
    creator_list = get_creator(tree)
    assert len(creator_list) != 0, "get_creator: creator (composer) not found"



def positive_test_check_element_match():
    """positive test for seeing if all elements in a file match themselves"""
    _,root = prepare_tree('database/Chopin.xml')
    all_equal = True
    unequalelt = None
    for element in root_to_list(root):
        if not check_element_match(element, element) :
            all_equal = False
            unequalelt = element
    assert all_equal, "check_element_match: Not all elements equal to themselves. Check Element with id "+ unequalelt.attrib["xml:id"]


def main():
    positive_test_find_expressive_term()
    positive_test_check_element_match()


if __name__ == '__main__':
    main()