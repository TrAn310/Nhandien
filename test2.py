import cv2

path = r'f:\lapTrinhPy\Q.jpg' #r là lệnh lấy đường dẫn của ảnh cần xử lý và gán với 1 biến đặt là path 
img1 = cv2.imread(path)

img=cv2.resize(img1,dsize=None,fx=0.3,fy=0.3)



gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# Tìm contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    # Lấy tọa độ bounding box cho mỗi contour
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Lọc bỏ các box quá nhỏ (nhiễu)
    if w > 10 and h > 10:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)

cv2.imshow('Result', img)
cv2.waitKey(0)