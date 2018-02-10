from lxml import etree
from tkinter.filedialog import askopenfilename
import tkinter

#tkinter.Tk().withdraw()
#tree = ET.parse(askopenfilename())

tree = etree.parse("chopin.xml")
root = tree.getroot()
namespace = "{http://www.music-encoding.org/ns/mei}"


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


def getTagList(root, tag):
    # returns list of all notes in order

    return [element.get(tag) for element in root.iter("note")]


def noteSearch(inputList, root):
    #inputList = search criteria, root = MEI file wh/ is being searched
    #returns index where sequence was found, -1 if not found

    # todo reformat lists (as input can be "abfdef")

    notesList = []
    idList = []
    i = 0
    xmlid = 23

    # todo if there are multiple matches
    # todo xml:id how to navegate through/ return the document?

    for element in root.iter(namespace + "note"):
        if i + 1 <= len(inputList):
            if inputList[i] == element.get("pname"):
                notesList.append(element.get("pname"))
                print(element.get("oct"))
                print("cur: ", notesList)
                if i == 0:
                    # print("find xml:id")
                    print(element.get("oct"))
                    print(element.get("xml"))
                    xmlid = element.get("xml:id")
                    print(xmlid)
                i +=1

            else:
                notesList.clear()
                i = 0

        else:
            print("hit the end of the input list, congrates you match!")
            idList.append(xmlid)
            notesList.clear()
            i = 0

    print("loop finish")

    if idList != []:
        return idList
    else:
        return "no exact match has been found"




def main():
    # criteria = ['f']
    # print(noteSearch(criteria, root))

    prepareTree(root)
    # print(getTagList(root, ))
    # print(getTagList(root, "oct"))
    # print(getTagList(root, "xml:id"))

    # testing for noteSearch:
    ls = ["a", "f", "b"]
    ls2 = ["c", "c", "c", "d"]
    print(noteSearch(ls2, root))
    # print("a")


if __name__ == "__main__":
    main()
