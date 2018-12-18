xrange = range

import numpy as np
import cv2 as cv

def make_image():
    img = np.zeros((500, 500), np.uint8)
    black, white = 0, 255
    for i in xrange(6):
        dx = int((i%2)*250 - 30)
        dy = int((i/2.)*150)

        if i == 0:
            for j in xrange(11):
                angle = (j+5)*np.pi/21
                c, s = np.cos(angle), np.sin(angle)
                x1, y1 = np.int32([dx+100+j*10-80*c, dy+100-90*s])
                x2, y2 = np.int32([dx+100+j*10-30*c, dy+100-30*s])
                cv.line(img, (x1, y1), (x2, y2), white)

        cv.ellipse( img, (dx+150, dy+100), (100,70), 0, 0, 360, white, -1 )
        cv.ellipse( img, (dx+115, dy+70), (30,20), 0, 0, 360, black, -1 )
        cv.ellipse( img, (dx+185, dy+70), (30,20), 0, 0, 360, black, -1 )
        cv.ellipse( img, (dx+115, dy+70), (15,15), 0, 0, 360, white, -1 )
        cv.ellipse( img, (dx+185, dy+70), (15,15), 0, 0, 360, white, -1 )
        cv.ellipse( img, (dx+115, dy+70), (5,5), 0, 0, 360, black, -1 )
        cv.ellipse( img, (dx+185, dy+70), (5,5), 0, 0, 360, black, -1 )
        cv.ellipse( img, (dx+150, dy+100), (10,5), 0, 0, 360, black, -1 )
        cv.ellipse( img, (dx+150, dy+150), (40,10), 0, 0, 360, black, -1 )
        cv.ellipse( img, (dx+27, dy+100), (20,35), 0, 0, 360, white, -1 )
        cv.ellipse( img, (dx+273, dy+100), (20,35), 0, 0, 360, white, -1 )
    return img

img = make_image()
cv.imshow('image', img)
cv.waitKey()
cv.destroyAllWindows()
