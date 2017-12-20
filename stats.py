import lxml.etree as et
import os
import sys
from xml.etree.ElementTree import  parse
import shutil
import json
from PIL import Image
fClassLabels = open('./classLabels.txt','r')


dir = os.path.dirname(os.path.abspath(__file__))
print("\nPath of this Python Script:"+dir)


label_list = {}

#NumOfLabels
#NumOfImages
#NumOfAnnotationsDone
#NumOfPersons
#NumOfSkippedImages
miscStats = {'NumOfLabels':0, 'NumOfTotalImages':0, 'NumOfAnnotationsDone':0, 'NumOfPersons':0, 'NumOfSkippedImages':0}
miscStats['NumOfTotalImages'] = len(os.walk(os.path.join(dir, "Images/example_folder")).next()[2])

# Reading the class labels to make dictionary that will store label counts. Initialize with 0
for eachLine in fClassLabels:
   label_list[eachLine.split()[0]] = 0
fClassLabels.close()

print 'Number of Labels: ',len(label_list)
miscStats['NumOfLabels'] = len(label_list)

print '\nClassification Labels:\n',label_list

noOfXMLFiles = len(os.walk(os.path.join(dir, "Annotations/example_folder")).next()[2])

print('{}{}'.format('Number of Annotated XML files: ',noOfXMLFiles))


# Reading Annotated XML files
xml_list = []
fileIndex = 0

annotationFolderPath = os.path.join(dir, 'Annotations/example_folder')
print("annotationFolderPath Value: "+annotationFolderPath)
for file in os.listdir(annotationFolderPath):
    if fileIndex == noOfXMLFiles:
        break
    fileIndex += 1
    if file.endswith(".xml"):
        xml_list.extend(file.split())
    
print '\nList of XML filenames:\n',xml_list
miscStats['NumOfAnnotationsDone'] = len(xml_list)

k = 0
import xml.etree.ElementTree

while(k<len(xml_list)):
    skipFile = False
    xmlFileName = xml_list[k]
    # Load an XML file into the tree and get the root element.
    print 'processing...Annotations/example_folder/',xmlFileName
    xmlFile = xml.etree.ElementTree.ElementTree(file=os.path.join(dir, 'Annotations/example_folder/'+xmlFileName))

    root = xmlFile.getroot()
    
    objects = root.findall('object')
    tmpLabelCountList = {}
    objectNameKey = ""
    for object in objects:
        objectName = object.findtext('name')
        objectNameKey = objectName.replace(" ","").lower()
        tmpLabelCountList[objectNameKey] = 0

    for object in objects:
        objectName = object.findtext('name')
        objectNameKey = objectName.replace(" ","").lower()
        
        if objectNameKey == 'skip':
            skipFile = True
            tmpLabelCountList[objectNameKey] = tmpLabelCountList[objectNameKey] + 1
            miscStats['NumOfSkippedImages'] = miscStats['NumOfSkippedImages'] + 1
            break

        if 'person' in objectNameKey:
            miscStats['NumOfPersons'] = miscStats['NumOfPersons'] + 1
        tmpLabelCountList[objectNameKey] = tmpLabelCountList[objectNameKey] + 1
        
    print 'Tmp Label Counts from Annotation file: ',xmlFileName,'\n',tmpLabelCountList

    if skipFile == False:
        # Add to the main list
        print 'Adding...'
        for (key, value) in tmpLabelCountList.items():
            if key in label_list:
                label_list[key] = label_list[key]+1

    else:
        print 'File ',xmlFileName,' is skipped...'

    k = k+1

print '\nFinal Class Labels Count:\n',label_list

print '\nMiscellaneous Statistics:\n',miscStats

# Writing above stats to json file
finalStats = {'labelClassCount':label_list, 'miscStats':miscStats}
fileStatsJSON = open('statsJSON.json','w')
fileStatsJSON.write(str(finalStats))
fileStatsJSON.close()
