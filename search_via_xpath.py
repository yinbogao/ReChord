from lxml import etree

tree = etree.parse("chopin.xml")
root = tree.getroot()
namespace = 'http://www.music-encoding.org/ns/mei'
note_namespace = 'http://www.w3.org/XML/1998/namespace'


def trial():
    r = tree.xpath('//mei:note[@xml:id]',
                   namespaces = {'mei': 'http://www.music-encoding.org/ns/mei'})
    print(r[0].attrib)
    tree.getpath(r[0])
    r[0].getparent()
    return r


def get_notes(tree):
    """return all the notes from the tree """

    # select all the note elements
    r = tree.xpath('//mei:note',
                   namespaces = {'mei': 'http://www.music-encoding.org/ns/mei'})

    # loop through r to get attrib dictionary, and select 'pname' key's value add to the list
    return [note.attrib['pname'] for note in r]

def notes_on_beam(tree):
    """return a list of nested list where each nested list is the notes on a beam"""

    # get a list of all the beam elements
    r = tree.xpath('//mei:beam',
                   namespaces={'mei': 'http://www.music-encoding.org/ns/mei'})
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

# print(trial())
print(get_notes(tree))
print(notes_on_beam(tree))