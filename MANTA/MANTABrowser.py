import cv2
import numpy as np
import json
import os

# Folder to read data
mantadir = 'P:/Python/python3/openCV/MANTA/DATASTORE/'
#mantadir = '//HOMEOFFICE/TRANSFER/RCOLSON/MANTA Data/'
# Blank image to display metadata  
metadata_image = np.full((800,600,3), 10, dtype=np.uint8)

def shadowText(argImg, argText, argX, argY):
    cv2.putText(argImg, argText, (argX-2, argY-2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX-2, argY+2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX+2, argY-2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX+2, argY+2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX, argY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    return

def writeLine(argImg, argDict, argElement, argRow):
    cv2.putText(argImg, argElement + ': ' + str(argDict[argElement]), (10, (argRow*20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    return

def dynamicMetadataDisplay(argImg, argText):
    # Clear the image with a filled rectangle
    cv2.rectangle(argImg, (0,0), (600,800), (255,255,255), -1)
    metadataDict = json.loads(argText)
    index = 1
    for element in metadataDict:
        writeLine(argImg, metadataDict, element, index)
        index += 1

# get the photos in the MANTA folders
for root, dirs, filenames in os.walk(mantadir):
    imgfiles = [file for file in filenames if file.endswith(('.jpg','.png'))]
    for f in imgfiles:
        jpgName = os.path.join(root,f)
        jsonName = jpgName.split('.')[0] + '.json'
        mantaImage = cv2.imread(jpgName)
        with open(jsonName, "r") as JSONfile:
            JSONtext = JSONfile.read()
            JSONfile.close()
        
            # Resize the image
            height, width, channels = mantaImage.shape
            if height >= width:
                mantaImage = cv2.resize(mantaImage, (600,800))
            else:
                mantaImage = cv2.resize(mantaImage, (800,600))
            
            # Display the capture type stored within the MANTA datastore with black shadow
            dirName = f.split('_')[0]
            shadowText(mantaImage, 'Classification - ' + dirName, 10, 15)
            # Display classification keys
            shadowText(mantaImage, 'ESC-Next', 10, 45)
            shadowText(mantaImage, 'Q-Quit', 10, 65)
            # Display the image
            cv2.imshow('MANTA IMAGE', mantaImage)
            # Get the formatted JSON
            pythondata = json.loads(JSONtext)
            formattedJSON = json.dumps(pythondata, indent=4)
            # Display the metadata and the image
            dynamicMetadataDisplay(metadata_image, formattedJSON)
            cv2.imshow('METADATA', metadata_image)
    
            # Wait for the user to press a key and take the appropriate action
            while True:
                ch = cv2.waitKey(5)
                # ESC key
                if ch == 27:
                    break 
                # Q key
                elif ch == 113:
                    print('Exiting the program...')
                    exit()

print('Done!')
cv2.destroyAllWindows()
