import os
import re
import sys
from classes.ListWithPaths import ListWithPaths
import xml.etree.ElementTree as ET

def search_manifest(output_dir, child_tag):
    children = ListWithPaths()
    child_tag = child_tag.lower()
    output_dir = output_dir + '/resources/AndroidManifest.xml'
    if os.path.exists(output_dir):
        tree = ET.parse(output_dir)
        root = tree.getroot()
        main_package = root.attrib['package']
        for child in root:
            if child_tag.split('/')[0] == "application":
                for sub_child in child:
                    if sub_child.tag == child_tag.split('/')[1]:
                            children.add(sub_child.attrib['{http://schemas.android.com/apk/res/android}name'],
                                              '/resources/AndroidManifest.xml')
            elif child.tag == child_tag:
                children.add(child.attrib['{http://schemas.android.com/apk/res/android}name'], '/resources/AndroidManifest.xml')

    else:
        return None

    return(children)