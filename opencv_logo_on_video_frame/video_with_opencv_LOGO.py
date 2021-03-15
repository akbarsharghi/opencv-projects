import cv2


img = cv2.imread('opencv.png')
rows, cols, _ = img.shape


imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(imgGray, 22, 255, cv2.THRESH_BINARY)
maskInv = cv2.bitwise_not(mask)
imgFG = cv2.bitwise_and(img, img, mask = mask)

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    maskInv = cv2.bitwise_not(mask)
    roi = frame[0:rows, 0:cols]
    
    imgBG = cv2.bitwise_and(roi, roi, mask = maskInv)
    dst = cv2.add(imgFG, imgBG)
    
    frame[0:rows, 0:cols] = dst
    cv2.imshow("winname", frame)
    
    if cv2.waitKey(4) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()