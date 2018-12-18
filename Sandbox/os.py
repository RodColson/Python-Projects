import os

# Set the base search directory
maindir = 'P:/Python/python3/openCV/MANTA/DATASTORE/'
#maindir = '//HOMEOFFICE/TRANSFER/RCOLSON/MANTA Data/'

#from os.path import join, getsize
#for root, dirs, files in os.walk(maindir):
    #print(root, "consumes", end=" ")
    #print(sum([getsize(join(root, name)) for name in files]), end=" ")
    #print("bytes in", len(files), "non-directory files")
    #if 'CVS' in dirs:
        #dirs.remove('CVS')  # don't visit CVS directories
        

## Get a total count of specific filetypes in the folder and subfolders
imgcount = sum([len([file for file in files if file.endswith(('.jpg','.png'))]) for r, d, files in os.walk(maindir)])
print('Total images found: {}'.format(imgcount))

for parentdir, subdirs, filenames in os.walk(maindir):
    for r in subdirs:
        print(parentdir)
        print(r)
      
        dirpath = os.path.join(parentdir,r)
        dirpaths.append(dirpath)
        print(dirpath)
        dirnum += 1
        
    #for f in filenames:
        #print(parentdir)
        #print(f)
        
        
    #imgfiles = [file for file in filenames if file.endswith(('.jpg','.png'))]
    #print('root: {}'.format(len(root)))
    #print('dirs: {}'.format(len(dirs)))
    #print('filenames: {}'.format(len(filenames)))
    #print('imgfiles: {}'.format(len(imgfiles)))
    #for f in imgfiles:
        #jpgName = os.path.join(root,f)
        #print(jpgName)
        
        
        
        
        
#for root, dirs, filenames in os.walk(maindir):
    ## select only files with specfic extensions
    #imgfiles = [file for file in filenames if file.endswith(('.jpg','.png'))]
    #print(len(imgfiles))
    #for f in imgfiles:
        #print(f)