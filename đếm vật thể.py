import cv2
import numpy as np
def empty():
    pass
cv2.namedwindow("trackbars")
cv2.resizeWindow("trackbars", 640, 100)
cv2.createtrackebar("value","trackbars",0,255,empty)
while True:
    cv2.imread("C:\Users\Admin\Pictures\Saved Pictures\dogs.webp")
    cv2.imshow("anh goc",img)
    #chuyen sang anh grayscale
    gray= cv2.ctvColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("anh gray",gray)
    #lam mo anh
    blur = cv2.GaussianBlur(gray,(5,5),0)
    value=cv2.getTrackbarPos("value","trackbars")
    #phan nguong anh va tao anh nhi phan
    thres=cv2.threshold(blur,value,255,cv2.THRESH_BINARY)
    cv2.imshow("anh nhi phan",thresh)
    #tim contours trong anh nhi phan
    contours= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #lap qua contours va ve chung len hinh anh
    cv2.drawContours(img,contours,-1,(0,255,0),2)
    #hien thi hinh anh voi contours da ve
    cv2.imshow("contours",img)
    cv2.waitkey(1)
    cv2.destroyAllWindows()
    #in ra so luong contours, tuc so luong vat the
    print(f"so luong vat the: {len(contours)}")


