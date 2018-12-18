#import struct
import pyodbc
import base64
import cv2

# Folder to save data
refdir = './MANTA/DATASTORE/'

# This function is needed when accessing datetimeoffset columns
#def handle_datetimeoffset(dto_value):
    ## ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    #tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    #tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    #return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# server = 'tcp:myserver.database.windows.net' 
server = 'tcp:hsbeu1-w00005.am.munichre.com' 
database = 'MANTA' 
username = 'mantaapp' 
password = '' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#cnxn.add_output_converter(-155, handle_datetimeoffset)

# Select query
# Processed through 3658 records on 12/11/2018 (last media_data_id 3659)

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
    
    # Write the image to the filesystem
    jpgName = refdir + captureType + '_' + fileName
    with open(jpgName, 'wb') as f:
        f.write(jpgData)

    # Write the metadata to the filesystem
    metadataName = refdir + captureType + '_' + fileName.split('.')[0] + '.json'
    with open(metadataName, 'wt') as f:
        f.write(metadata)

    row = cursor.fetchone()

print('Done!')
