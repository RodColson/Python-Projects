#import struct
import pyodbc
import base64
import cv2
import numpy as np
import json
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--env", required=True, help="DB environment (DEV/STAGE/PROD)")
ap.add_argument("-s", "--start", type=int, default=0, help="Starting media_metadata_id for processing")
args = vars(ap.parse_args())

# Database connection to use
DBENV = args["env"]

# Folder to save data
DSdir = './MANTA/DATASTORE/'
# Blank image to display metadata
metadata_image = np.full((800,600,3), 10, dtype=np.uint8)

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

def processPhoto(argCaptureType, argFileName, argJPG, argMetadata, argMediaID):
    # Determine the capType value to use
    if argCaptureType == 'Location':
        capType = '1'
    elif argCaptureType == 'Reference':
        capType = '2'
    elif argCaptureType == 'Number Plate':
        capType = '3'
    elif argCaptureType == 'Detail':
        capType = '4'
    else:
        print('Unknown capture type: {}'.format(argCaptureType))
        return

    # Update the record in the DB with the new classification
    SQLString = "UPDATE [MANTA].[manta].[media_metadata] SET media_capture_type_id = " + capType + " WHERE media_metadata_id = " + str(argMediaID) + ";"
    # Updates to the DB don't work in PROD for some reason.  Write UPDATE lines to a file for later processing
    with open("MANTA Updates.txt", "a") as f:
        f.write(SQLString)
        f.write("\n")
        # Close the file after each write.  We don't want to lose any data.
        f.close()

    #try:
        #updcursor.execute("UPDATE [MANTA].[manta].[media_metadata] SET media_capture_type_id = " + capType + " WHERE media_metadata_id = " + str(argMediaID) + ";")
    #except pyodbc.Error as ex:
        #sqlstate = ex.args[0]
        #print('SQL Error: {}'.format(sqlstate))
    #try:
        #updcursor.commit()
    #except pyodbc.Error as ex:
        #sqlstate = ex.args[0]
        #print('SQL Error: {}'.format(sqlstate))
    
    #print(updcursor.rowcount, "record(s) updated")
    
    ## Write the image to the filesystem
    #jpgName = DSdir + argCaptureType + '/' + argFileName
    #with open(jpgName, 'wb') as f:
        #f.write(argJPG)
    ## Write the metadata to the filesystem
    #metadataName = DSdir + argCaptureType + '/' + argFileName.split('.')[0] + '.json'
    #with open(metadataName, 'wt') as f:
        #f.write(metadata)
    return

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

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# server = 'tcp:myserver.database.windows.net' 
if DBENV == 'DEV':
    server = 'tcp:hsbeu1-w00001.am.munichre.com'
elif DBENV == 'STAGE':
    server = 'tcp:hsbeu1-w00003.am.munichre.com'
elif DBENV == 'PROD':
    server = 'tcp:hsbeu1-w00005.am.munichre.com'
else:
    print('Unknown Database Environment: {}'.format(DBENV))
    exit()

database = 'MANTA' 
username = 'mantaapp' 
password = '' 
try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print('SQL Error: {}'.format(sqlstate))
try:
    updcnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print('SQL Error: {}'.format(sqlstate))

cursor = cnxn.cursor()
updcursor = updcnxn.cursor()

#cnxn.add_output_converter(-155, handle_datetimeoffset)

# Select records starting with the MMI of the passed argument
startMMI = str(args["start"])
try:
    cursor.execute("SELECT B.file_name, C.name, A.media_object, B.attributes, B.media_metadata_id FROM [MANTA].[manta].[media_data] A JOIN [MANTA].[manta].[media_metadata] B ON A.media_metadata_id = B.media_metadata_id JOIN [MANTA].[enum].[media_capture_type] C ON B.media_capture_type_id = C.media_capture_type_id WHERE B.media_metadata_id >= " + startMMI + " ORDER BY B.media_metadata_id;") 
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print('SQL Error: {}'.format(sqlstate))

try:
    row = cursor.fetchone()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print('SQL Error: {}'.format(sqlstate))
    
rowcount = 0

while row:
    rowcount = rowcount + 1
    
    fileName = row[0]
    captureType = row[1]
    imgData = row[2]
    metadata = row[3]
    media_metadata_id = row[4]
    
    print('Processing row - {0}   MMI - {1}'.format(rowcount, media_metadata_id))

    imgText = imgData.decode("utf-8")
    jpgData = base64.b64decode(imgText.split(',')[1])
    
    # Prepare the image for user to classify
    cvimg = data_uri_to_cv2_img(jpgData)
    # Resize the image
    height, width, channels = cvimg.shape
    if height > width:
        cvimg = cv2.resize(cvimg, (600,800))
    else:
        cvimg = cv2.resize(cvimg, (800,600))
    # Display the capture type stored within the MANTA datastore with black shadow
    shadowText(cvimg, 'Current Classification - ' + captureType, 10, 15)
    # Display classification keys
    shadowText(cvimg, 'L-Location', 10, 45)
    shadowText(cvimg, 'R-Reference', 10, 65)
    shadowText(cvimg, 'D-Detail', 10, 85)
    shadowText(cvimg, 'P-Number Plate', 10, 105)
    shadowText(cvimg, 'ESC-Skip', 10, 125)
    shadowText(cvimg, 'Q-Quit', 10, 145)
    # Display the image
    cv2.imshow('MANTA IMAGE - ' + DBENV, cvimg)
    # Get the formatted JSON
    pythondata = json.loads(metadata)
    formattedJSON = json.dumps(pythondata, indent=4)
    # Display the metadata and the image
    dynamicMetadataDisplay(metadata_image, formattedJSON)
    cv2.imshow('METADATA - ' + DBENV, metadata_image)

    # Wait for the user to press a key and take the appropriate action
    while True:
        ch = cv2.waitKey(5)
        # L key
        if ch == 108:
            processPhoto('Location', fileName, jpgData, metadata, media_metadata_id)
            break
        # R key
        elif ch == 114:
            processPhoto('Reference', fileName, jpgData, metadata, media_metadata_id)
            break
        # P key
        elif ch == 112:
            processPhoto('Number Plate', fileName, jpgData, metadata, media_metadata_id)
            break
        # D key
        elif ch == 100:
            processPhoto('Detail', fileName, jpgData, metadata, media_metadata_id)
            break
        # Q key
        elif ch == 113:
            print('Exiting the program...')
            print('Last MMI processed: {}'.format(media_metadata_id))
            exit()
        # ESC key
        if ch == 27:
            break 
    row = cursor.fetchone()

print('Done!')
print('Last MMI processed: {}'.format(media_metadata_id))
cv2.destroyAllWindows()
