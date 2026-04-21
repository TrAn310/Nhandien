import cv2
import numpy as np

# Khởi tạo camera (0 thường là webcam mặc định của laptop)
cap = cv2.VideoCapture(0)

while True:
    # 1. Đọc khung hình từ camera
    ret, frame = cap.read()
    if not ret:
        break

    # 2. Chuyển đổi từ BGR sang HSV (Rất quan trọng cho đề tài)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 3. Định nghĩa dải màu vàng cho Mũ Bảo Hộ trong không gian HSV
    # Lưu ý: Các giá trị này có thể tinh chỉnh tùy theo môi trường ánh sáng
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # 4. Tạo mặt nạ (Mask) để lọc ra các vùng màu vàng
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 5. Khử nhiễu (Dùng Morphology - giúp mask mịn hơn)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 6. Tìm đường bao (Contours) của vùng màu vàng
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Chỉ nhận diện nếu vùng màu vàng đủ lớn (tránh nhận diện nhầm các đốm nhỏ)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            # Vẽ hình chữ nhật cảnh báo quanh mũ bảo hộ
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Safety Helmet (Yellow)", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 7. Hiển thị kết quả
    cv2.imshow("He thong giam sat An toan Lao dong", frame)
    cv2.imshow("Mat na loc mau (Mask)", mask)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('  '):
        break

cap.release()
cv2.destroyAllWindows()