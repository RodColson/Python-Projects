import struct
import pyodbc

def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
#server = 'tcp:myserver.database.windows.net' 
server = 'tcp:hsbeu1-w00005.am.munichre.com' 
database = 'MANTA' 
username = 'mantaapp' 
password = '' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cnxn.add_output_converter(-155, handle_datetimeoffset)

#Sample select query
cursor.execute("SELECT TOP 10 created_by, created_date FROM [MANTA].[manta].[media_data];") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()