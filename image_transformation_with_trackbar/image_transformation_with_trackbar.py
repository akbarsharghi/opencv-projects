import cv2
import numpy as np
import argparse


def nothing(x):
    pass


apz = argparse.ArgumentParser()
apz.add_argument('-i', '--image', required=True, help='Path to the image')
arg = vars(apz.parse_args())

image = cv2.imread(arg["image"])
cv2.namedWindow('Image')
# print(image.shape)

(h, w) = image.shape[:2]
center = (h // 2, w // 2)

# Create trackbar for image transformation
cv2.createTrackbar("Translation Down_Up", "Image", 0, 120, nothing)
cv2.createTrackbar("Translation Right_Left", "Image", 0, 120, nothing)
cv2.createTrackbar("Rotate", 'Image', 0, 360, nothing)
cv2.createTrackbar("Flapping", "Image", 0, 3, nothing)

# Create switch for save photo
switch = "Save"
cv2.createTrackbar(switch, 'Image', 0, 1, nothing)

while (1):

    # Get current position of trackbar
    rot = cv2.getTrackbarPos('Rotate', 'Image')
    tranDU = cv2.getTrackbarPos("Translation Down_Up", 'Image')
    tranRL = cv2.getTrackbarPos("Translation Right_Left", 'Image')
    flap = cv2.getTrackbarPos("Flapping", 'Image')

    save = cv2.getTrackbarPos(switch, 'Image')

    M_rotate = cv2.getRotationMatrix2D(center, rot, 1.0)

    if tranRL > 0 | tranDU > 0:
        M_trans = np.float32([[1, 0, tranDU], [0, 1, tranRL]])
        changed = cv2.warpAffine(image, M_trans, (image.shape[1], image.shape[0]))
        (w_ta, h_ta) = changed.shape[:2]
        center_ta = (w_ta // 2, h_ta // 2)
        M_rotate = cv2.getRotationMatrix2D(center_ta, rot, 1.0)
        changed = cv2.warpAffine(changed, M_rotate, (w_ta, h_ta))
        if flap == 0:
            pass
        elif flap == 1:
            changed = cv2.flip(changed, 1)
        elif flap == 2:
            changed = cv2.flip(changed, 0)
        elif flap == 3:
            changed = cv2.flip(changed, -1)
    else:
        M_trans = np.float32([[1, 0, tranDU], [0, 1, tranRL]])
        changed = cv2.warpAffine(image, M_trans, (image.shape[1], image.shape[0]))
        M_rotate = cv2.getRotationMatrix2D(center, rot, 1.0)
        changed = cv2.warpAffine(changed, M_rotate, (w, h))
        if flap == 1:
            changed = cv2.flip(changed, 1)
        elif flap == 2:
            changed = cv2.flip(changed, 0)
        elif flap == 3:
            changed = cv2.flip(changed, -1)
        elif flap == 0:
            pass

    cv2.imshow('Image', changed)

    if save == 0:
        pass
    else:
        cv2.imwrite('Changed.jpg', changed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
