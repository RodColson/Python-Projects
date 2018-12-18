#import struct
import pyodbc
import base64
import cv2
import numpy as np
import json
from tkinter import Tk, Label, Button
root = Tk()

# Make window 600x800 and place at position (50,50)
root.geometry("1600x900")

# Create a button with a custom callback
def my_callback():
    print("The button was clicked!")  # Prints to console not the GUI

# Create a button that will destroy the main window when clicked
exit_button = Button(root, text='Exit Program', command=root.destroy).grid(row=0, column=0)
print_button = Button(root, text='Click me!', command=my_callback).grid(row=0, column=1)

root.mainloop()

# Folder to save data
DSdir = './MANTA/DATASTORE/'
# Blank image to display metadata
metadata_image = np.zeros((800,600,3), np.uint8)

# This function is needed when accessing datetimeoffset columns
#def handle_datetimeoffset(dto_value):
    ## ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    #tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    #tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    #return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

def data_uri_to_cv2_img(uri):
    nparr = np.fromstring(uri, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def processPhoto(argCaptureType, argFileName, argJPG, argMetadata):
    # Write the image to the filesystem
    jpgName = DSdir + argCaptureType + '/' + argFileName
    with open(jpgName, 'wb') as f:
        f.write(argJPG)
    # Write the metadata to the filesystem
    metadataName = DSdir + argCaptureType + '/' + argFileName.split('.')[0] + '.json'
    with open(metadataName, 'wt') as f:
        f.write(metadata)
    return

def shadowText(argImg, argText, argX, argY):
    cv2.putText(argImg, argText, (argX-2, argY-2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX-2, argY+2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX+2, argY-2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX+2, argY+2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    cv2.putText(argImg, argText, (argX, argY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    return

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# server = 'tcp:myserver.database.windows.net' 
server = '' 
database = 'MANTA' 
username = 'mantaapp' 
password = '' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#cnxn.add_output_converter(-155, handle_datetimeoffset)

#Sample select query
cursor.execute("SELECT TOP 5 B.file_name, C.name, A.media_object, B.attributes FROM [MANTA].[manta].[media_data] A JOIN [MANTA].[manta].[media_metadata] B ON A.media_metadata_id = B.media_metadata_id JOIN [MANTA].[enum].[media_capture_type] C ON B.media_capture_type_id = C.media_capture_type_id;") 
row = cursor.fetchone()
rowcount = 0

while row:
    rowcount = rowcount + 1
    print('Processing row - {}'.format(rowcount))
    
    fileName = row[0]
    captureType = row[1]
    imgData = row[2]
    metadata = row[3]
    
    imgText = imgData.decode("utf-8")
    jpgData = base64.b64decode(imgText.split(',')[1])
    
    # Prepare the image for user to classify
    cvimg = data_uri_to_cv2_img(jpgData)
    # Display attributes
    pythondata = json.loads(metadata)
    formattedJSON = json.dumps(pythondata, indent=4)
    # Display the capture type stored within the MANTA datastore with black shadow
    shadowText(cvimg, 'Current Classification - ' + captureType, 10, 15)
    # Display classification keys
    shadowText(cvimg, 'L-Location', 10, 45)
    shadowText(cvimg, 'R-Reference', 10, 65)
    shadowText(cvimg, 'D-Detail', 10, 85)
    shadowText(cvimg, 'P-Number Plate', 10, 105)
    shadowText(cvimg, 'ESC-Skip', 10, 125)
    # Display the image
    cv2.imshow('MANTA IMAGE', cvimg)
    # Display the metadata
    metadataText(metadata_image, formattedJSON, 10, 15)
    cv2.imshow('METADATA', metadata_image)

    while True:
        ch = cv2.waitKey(5)
        # L key
        if ch == 108:
            processPhoto('Location', fileName, jpgData, metadata)
            break
        # R key
        elif ch == 114:
            processPhoto('Reference', fileName, jpgData, metadata)
            break
        # P key
        elif ch == 112:
            processPhoto('Number Plate', fileName, jpgData, metadata)
            break
        # D key
        elif ch == 100:
            processPhoto('Detail', fileName, jpgData, metadata)
            break
        # ESC key
        if ch == 27:
            break 
    row = cursor.fetchone()

print('Done!')
cv2.destroyAllWindows()
