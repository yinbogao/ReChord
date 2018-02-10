from lxml import etree
from tkinter.filedialog import askopenfilename
import tkinter

#tkinter.Tk().withdraw()
#tree = ET.parse(askopenfilename())

tree = etree.parse("chopin.xml")
root = tree.getroot()

def prepareTree(root):
    # remove html text from tags

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

    # todo reformat lists (as input can be "abfdef")

    notesList = []
    xmlIDs = []
    i = 0
    ID = ""

    # todo if there are multiple matches
    # todo xml:id how to navegate through/ return the document?
    for element in root.iter("note"):
        try:
            if inputList[i] == element.get("pname"):
                notesList.append(element.get("pname"))
                print("cur: ", notesList)
                if i == 0:
                    print("find xml:id")
                    ID = element.get("xml:id")
                    # print(xmlID)
                i +=1

            else:
                notesList.clear()
                i = 0
        except IndexError:
            print("hit the bottom, congrates you match!")
            xmlIDs.append(ID)
            i = 0
            continue

    print("loop finish")

    if set(notesList) | set(inputList) == set(notesList) & set(inputList):

        return xmlIDs
    else:
        return "no exact match has been found"




def main():
    # criteria = ['f']
    # print(noteSearch(criteria, root))

    prepareTree(root)
    # print(getNotesList(root))

    # testing for noteSearch:
    ls = ["a", "f", "b"]
    ls2 = ["c", "c", "c", "d"]
    print(noteSearch(ls2, root))
    # print("a")


if __name__ == "__main__":
    main()
