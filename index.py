#!/usr/bin/python
# -*- coding:utf-8 -*-
from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2


#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True, help = "Path to the direction that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True, help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

#initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

#open the output index file for writing
output = open(args["index"], "w")

#use glob to grab the image paths and loop over them
for imagePath in glob.glob(args["dataset"] + "/*.jpg"):
    #extract the image ID (i.e. the unique filename) from the image path and load the image itself
    imageID = imagePath[imagePath.rfind("/") + 1:]
    imageID = imageID.replace('########','/')    
    if(imageID[-5] == ')'):
        imageID = imageID[:-7] + imageID[-4:]
    print ("正在建立图片"+imageID+"的索引")
    try:
        image = cv2.imread(imagePath)
        #descriptor the image
        features =  cd.descriptor(image)
    except:
        print ("建立失败") 
    else:
        #write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imageID, ",".join(features)))
        print ("建立成功")
for imagePath in glob.glob(args["dataset"] + "/*.png"):
    #extract the image ID (i.e. the unique filename) from the image path and load the image itself
    imageID = imagePath[imagePath.rfind("/") + 1:]
    imageID = imageID.replace('########','/')    
    if(imageID[-5] == ')'):
        imageID = imageID[:-7] + imageID[-4:]
    print ("正在建立图片"+imageID+"的索引")
    try:
	#descriptor the image
        image = cv2.imread(imagePath)
        features =  cd.descriptor(image)
    except:
        print ("建立失败") 
    else:
        #write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imageID, ",".join(features)))
        print ("建立成功")

#close the index file
output.close()


