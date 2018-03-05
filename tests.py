from search import prepare_tree, find_expressive_term, get_measure

tree, _ = prepare_tree('database/Chopin.xml')
element_et_list = find_expressive_term(tree, 'legatissimo')
assert len(element_et_list) != 0, "find_expressive_term: legatissimo not found."
