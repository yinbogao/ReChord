import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
import tkinter

#tkinter.Tk().withdraw()
#tree = ET.parse(askopenfilename())
tree =ET.parse("chopin.xml")

root = tree.getroot()

for child in root:
    for child2 in child:
        print(child2.tag)
        print(child2.attrib)
    print()
