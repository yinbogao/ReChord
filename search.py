import xml.etree.ElementTree as ET

# parse through the given file & pass value to tree and root
tree = ET.parse('Chopin.xml')
root = tree.getroot()


### below are tests, feel free to delete
    # these tests only able to spit memory location as result so far
print(root.keys)

for child in root:
    print(child.tag, child.attrib, child.text)

element_ls= ET.SubElement(root, "persName")
print(element_ls)

