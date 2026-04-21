import cv2
import numpy as np
path = r"C:\Users\Admin\Pictures\Saved Pictures\banh-quy.webp"
img=cv2.imread(path)
# def empty():
#     pass
# cv2.namedWindow("trackbars")
# cv2.resizeWindow("trackbars",640,100)
# cv2.createTrackbar("value","trackbars",0,255,empty)
while True:
    cv2.imread(path)
    cv2.imshow("anh goc",img)
    #chuyen sang anh grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("anh gray",gray)
    # lam mo
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # phan nguong anh va tao anh nhi phan
    _,thresh = cv2.threshold(blur,155, 255, cv2.THRESH_BINARY_INV)
    #tim contours trong anh nhi phan
    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    cv2.imshow("anh nhi phan", thresh)
    cv2.waitKey(0)


