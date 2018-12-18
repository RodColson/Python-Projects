import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

def unwarp(img, src, dst, testing):
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)

    if testing:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        f.subplots_adjust(hspace=.2, wspace=.05)
        ax1.imshow(img)
        x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
        y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
        ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
        ax1.set_ylim([h, 0])
        ax1.set_xlim([0, w])
        ax1.set_title('Original Image', fontsize=30)
        ax2.imshow(cv2.flip(warped, 1))
        ax2.set_title('Unwarped Image', fontsize=30)
        plt.show()
    else:
        return warped, M


im = cv2.imread(".\img\DataPlate6.jpg")

h, w = im.shape[0], im.shape[1]
print("w: {} h: {}".format(w, h))
# We will first manually select the source points 
# we will select the destination point which will map the source points in
# original image to destination points in unwarped image
src = np.float32([(1,     1),
                  (4031,  70),
                  (1,    2990),
                  (3990,  2920)])

dst = np.float32([(w, 0),
                  (0, 0),
                  (w, h),
                  (0, h)])

unwarp(im, src, dst, True)

cv2.imshow("Corrected", im)

cv2.waitKey(0)
cv2.destroyAllWindows()
