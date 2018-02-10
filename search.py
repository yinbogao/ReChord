from lxml import etree
from tkinter.filedialog import askopenfilename
import tkinter

#tkinter.Tk().withdraw()
#tree = ET.parse(askopenfilename())

tree = etree.parse("chopin.xml")
root = tree.getroot()


def recursiveElementList(root, i):
    #for n in range(1, i):
    # print("    ", end = "")

    root.tag = root.tag.replace("{http://www.music-encoding.org/ns/mei}", "")
    spaces = ""
    for n in range(0, i):
        spaces += "  "

    print(spaces + "<" + root.tag + ">")
    if (root.tag == 'note'):
        print(spaces + " " + root.attrib['pname'])

    spaces = ""

    if len(root):
        for child in root:
            recursiveElementList(child, i + 1)


def getNotesList(root, i, list):
    # returns list of all notes in order

    # check if element is a note, then if it is, add it's letter to the list.
    if (root.tag.replace("{http://www.music-encoding.org/ns/mei}",
                         "") == 'note'):
        list.append(root.attrib['pname'])
    if len(root):
        for child in root:
            getNotesList(child, i + 1, list)
    return list


def noteSearch(inputList, root):
    #inputList = search criteria, root = MEI file wh/ is being searched
    #returns index where sequence was found, -1 if not found

    noteList = ['a', 'b', 'c', 'd', 'e', 'f']

    #noteList = getNotesList(root, 0, [])

    for i in range(0, len(noteList) - len(inputList) + 1):
        j = 0
        while (noteList[i + j] == inputList[j]):
            if (j == len(inputList) - 1):
                return i
            j += 1
    return -1


criteria = ['f']
print(noteSearch(criteria, root))

for i in getNotesList(root, 0, []):
    print(i, end=", ")
