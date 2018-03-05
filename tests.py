from search import prepare_tree, find_expressive_term, get_measure

def positive_test_find_expressive_term():
    """Positive test for find_expressive_term"""
    tree, _ = prepare_tree('database/Chopin.xml')
    element_et_list = find_expressive_term(tree, 'legatissimo')
    assert len(element_et_list) != 0, "find_expressive_term: legatissimo not found."

def main():
    positive_test_find_expressive_term()

if __name__ == '__main__':
    main()
