import cv2

filename = './openCV/MANTA/DATASTORE/Location_Image_JGC662CDU6VZW8Y6URD.jpg'

inputImage = cv2.imread(filename)
cv2.imshow("Input Photo", cv2.resize(inputImage, (0,0), fx=0.1, fy=0.1))

while True:
    ch = cv2.waitKey(500)
    print('Key Code: {}'.format(ch))
    if ch == 27:
        break    
