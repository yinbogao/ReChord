from search import prepare_tree, find_expressive_term, get_measure, check_element_match, tree_to_list


def positive_test_find_expressive_term():
    """Positive test for find_expressive_term"""
    tree, _ = prepare_tree('database/Chopin.xml')
    element_et_list = find_expressive_term(tree, 'legatissimo')
    assert len(element_et_list) != 0, "find_expressive_term: legatissimo not found."


def positive_test_check_element_match():
    """positive test for seeing if all elements in a file match themselves"""
    _,root = prepare_tree('database/Chopin.xml')
    all_equal = True
    unequalelt = None
    for element in tree_to_list(root):
        if not check_element_match(element, element) :
            all_equal = False
            unequalelt = element
    assert all_equal, "check_element_match: Not all elements equal to themselves. Check Element with id "+ unequalelt.attrib["xml:id"]


def main():
    positive_test_find_expressive_term()


if __name__ == '__main__':
    main()
