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


    ls = [child.attrib for child in r[0]]
    beam_note = []
    for dic in ls:
        beam_note += dic['pname']
    return r


def notes_on_beam(tree):
    """return all the notes (in a list) from all the beam in a overall list """

    # select all the beam element
    r = tree.xpath('//mei:beam',
                   namespaces = {'mei': 'http://www.music-encoding.org/ns/mei'})
    notes_in_beam = []

    # loop through all the element and create a attribute dictionary for each element
    for i in range(len(r)):
        ls = [child.attrib for child in r[i]]

        # add all note from a beam to a list
        beam_note = [dic['pname'] for dic in ls]

        # append the beam list to the whole list
        notes_in_beam += beam_note
    return notes_in_beam


print(trial())
print(notes_on_beam(tree))