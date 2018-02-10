from lxml import etree
from tkinter.filedialog import askopenfilename
import tkinter

#tkinter.Tk().withdraw()
#tree = ET.parse(askopenfilename())

tree = etree.parse("chopin.xml")
root = tree.getroot()

def prepareTree(root):
    for element in root.iter():
        element.tag = element.tag.replace("{http://www.music-encoding.org/ns/mei}", "")
    return


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


def getNotesList(root):
    # returns list of all notes in order

    return [element.get("pname") for element in root.iter("note")]


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



def main():
    # criteria = ['f']
    # print(noteSearch(criteria, root))
    prepareTree(root)
    print(getNotesList(root))


if __name__ == "__main__":
    main()
