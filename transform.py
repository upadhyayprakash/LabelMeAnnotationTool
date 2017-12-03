#!/usr/bin/env python
import lxml.etree as et
import os
import sys
from xml.etree.ElementTree import  parse
import shutil 
#fh1 = open('/data/LabelMeAnnotationTool/annotationCache/DirLists/labelme.txt','r')

#import pdb
#pdb.set_trace()

img_list = []

#for eachLine in fh1:
#    img_list.extend(eachLine.split())
#fh1.close()


dir = os.path.dirname(os.path.abspath(__file__))
#os.path.dirname(os.path.abspath(__file__))
print("Path of script:"+dir)
#noOfFiles = len(os.walk(os.path.join(dir, "/Annotations/example_folder")).next()[2])


noOfFiles = len(os.walk(os.path.join(dir, "Annotations/example_folder")).next()[2])

print('{}{}'.format('Number of files: ',noOfFiles))

fileIndex = 0

# I319452: read only annotated file names for copy and traversing.
#for file in os.listdir("/data/LabelMeAnnotationTool/Annotations/example_folder"):
pathreal = os.path.join(dir, 'Annotations/example_folder')
print("PathReal Value: "+pathreal)
for file in os.listdir(pathreal):
    if fileIndex == noOfFiles:
        break
    fileIndex += 1
    if file.endswith(".xml"):
        img_list.extend(file.split())
    
print(img_list)
k = 0
while(k<len(img_list)):
#    imname = img_list[k].split(",")

    #required to get the images from subfolder from example_folder thye path is given in labelme.txt
#    subdirectorypath=imname[-2]
#    imname = imname[-1]
    imname = img_list[k]
    imagename=imname
    imname = imname[:-4]
    annotatedfilepath=os.path.join(dir, 'PVOC/'+imname+'.xml')
    print('PVOC Path formed...')       
    xml2 = open(annotatedfilepath,'w')
    print(xml2)




    def gen_xml_object(xmin, xmax, ymin, ymax, objectName, date, id, occluded, hasparts, ispartof):

        xml_object = et.Element('object')
        xml_xmin = et.Element('xmin')
        xml_xmax = et.Element('xmax')
        xml_ymin = et.Element('ymin')
        xml_ymax = et.Element('ymax')
        xml_bndbox = et.Element('bndbox')
        xml_objectName = et.Element('name')
        xml_date = et.Element('date')
        xml_id = et.Element('id')
        xml_occluded = et.Element('occluded')
        xml_hasparts = et.Element('hasparts')
        xml_ispartof = et.Element('ispartof')
        xml_objectName.text = str(objectName)
        xml_date.text = str(date)
        xml_id.text = str(id)
        xml_occluded.text = str(occluded)
        xml_hasparts.text = str(hasparts)
        xml_ispartof.text = str(ispartof)
        xml_xmin.text = str(xmin)
        xml_xmax.text = str(xmax)
        xml_ymin.text = str(ymin)
        xml_ymax.text = str(ymax)
        xml_object.append(xml_objectName)
        xml_object.append(xml_date)
        xml_object.append(xml_id)
        
        xml_object.append(xml_occluded)
        xml_object.append(xml_hasparts)
        xml_object.append(xml_ispartof)
        
        xml_object.append(xml_bndbox)
        xml_bndbox.append(xml_xmin)
        xml_bndbox.append(xml_xmax)
        xml_bndbox.append(xml_ymin)
        xml_bndbox.append(xml_ymax)
                                     
        return xml_object




    def gen_coordinate_images_copy(annotatedfilepath,image_name):
             image_name = image_name + '.jpg'
            #directory to save the images 

             imagesavedir= os.path.join(dir, 'Images/example_folder')
             imagecopydir = os.path.join('SelectedImages')

             
             #the name for which the copy needs to be made
             image=imagesavedir+'/'+image_name

             print (os.path.basename(annotatedfilepath))
             doc = parse(annotatedfilepath)
             root = doc.getroot()

             image_name_text = image_name.split('.')[-2]

             for idx,rootobject in enumerate(root.findall("object")):
                                                                          
                 for bndboxobj in rootobject.findall('bndbox'):   
                     for xmin,xmax,ymin,ymax in zip(bndboxobj.iter('xmin'),bndboxobj.iter('xmax'),bndboxobj.iter('ymin'),bndboxobj.iter('ymax')):
                         shutil.copyfile(image,imagecopydir+'/'+ image_name_text+'_'+str(idx)+'_'+xmin.text+'_'+ymin.text+'_'+xmax.text+'_'+ymax.text+'.jpg')
    def gen_xml():

        xml2 = et.Element('annotation')
        xml_name = et.Element('filename')
        xml_folder = et.Element('folder')
                                        # Load an XML file into the tree and get the root element.

        import xml.etree.ElementTree
        xml = xml.etree.ElementTree.ElementTree(file=os.path.join(dir, 'Annotations/example_folder/'+imname+'.xml'))

        root = xml.getroot()
        filename = root.findtext('filename')
        xml_name.text = str(filename)
        xml2.append(xml_name)
        folder = root.findtext('folder')
        xml_folder.text = str(folder)
        xml2.append(xml_folder)

        objects = root.findall('object')
        for object in objects:

            objectName = object.findtext('name')
            date = object.findtext('date')
            id = object.findtext('id')
            occluded = object.findtext('occluded')
            parts1 = object.findall('parts')
            hasparts = None
            ispartof = None
            for parts in parts1:                                                                                                                                                                                        hasparts = parts.findtext('hasparts')
               # ispartof = parts.findtext('ispartof')

            polygons = object.findall('polygon')
            for polygon in polygons:

                pts = polygon.findall('pt')
                xList = []
                yList = []
                object1 = {'xmin': 0, 'xmax': 0, 'ymin': 0, 'ymax': 0}
                for pt in pts:
                    xList.append(pt.findtext('x'))
                    yList.append(pt.findtext('y'))
                object1['xmin'] = xList[-1]
                object1['xmax'] = xList[1]
                object1['ymin'] = yList[1]
                object1['ymax'] = yList[-1]
                xml2.append(gen_xml_object(object1['xmin'], object1['xmax'], object1['ymin'], object1['ymax'], objectName, date, id, occluded, hasparts, ispartof))
        return xml2

    print(str(et.tostring(gen_xml())))    
    xml2.write(str(et.tostring(gen_xml())))
    xml2.close()
    gen_coordinate_images_copy(annotatedfilepath,imname)
    k = k + 1
