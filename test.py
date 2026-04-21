import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import os

class FingerPaintApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW) # Sử dụng CAP_DSHOW để tăng khả năng tương thích

        if not self.vid.isOpened():
            print("Không thể mở camera. Vui lòng kiểm tra lại thiết bị hoặc quyền truy cập.")
            self.window.destroy()
            return

        self.canvas_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.canvas_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # Tạo một 'bảng vẽ' màu đen để lưu các đường vẽ
        self.paint_board = np.zeros((self.canvas_height, self.canvas_width, 3), np.uint8) 

        # Nút để xóa bảng vẽ
        self.btn_clear = tk.Button(window, text="Xóa bảng vẽ", width=20, 
                                   command=self.clear_board, bg="#f44336", fg="white")
        self.btn_clear.pack(padx=10, pady=5)
        
        # Nút để thoát
        self.btn_exit = tk.Button(window, text="Thoát", width=20, 
                                  command=self.window.destroy, bg="#555555", fg="white")
        self.btn_exit.pack(padx=10, pady=5)

        # Cài đặt dải màu đỏ (HSV)
        # Giá trị thấp của màu đỏ (màu đỏ nằm ở cả 2 đầu của phổ HSV)
        self.lower_red1 = np.array([0, 100, 100])
        self.upper_red1 = np.array([10, 255, 255])
        # Giá trị cao của màu đỏ
        self.lower_red2 = np.array([160, 100, 100])
        self.upper_red2 = np.array([179, 255, 255])

        self.delay = 10
        self.update()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing) # Xử lý khi đóng cửa sổ
        self.window.mainloop()

    def clear_board(self):
        # Thiết lập lại bảng vẽ thành màu đen hoàn toàn
        self.paint_board = np.zeros((self.canvas_height, self.canvas_width, 3), np.uint8)
        print("Đã xóa bảng vẽ.")

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1) # Lật ảnh để nó giống như gương

            # Chuyển đổi từ BGR sang HSV
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Tạo mask cho màu đỏ
            mask1 = cv2.inRange(hsv_frame, self.lower_red1, self.upper_red1)
            mask2 = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)
            mask = mask1 + mask2 # Kết hợp hai mask lại

            # Xử lý hình thái học để làm mịn mask và loại bỏ nhiễu
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))

            # Tìm đường bao (contours) trong mask
            contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Tìm đường bao lớn nhất (giả sử là ngón tay/vật thể)
                max_contour = max(contours, key=cv2.contourArea)
                
                # Chỉ xử lý nếu đường bao đủ lớn để tránh nhiễu
                if cv2.contourArea(max_contour) > 500: # Ngưỡng diện tích nhỏ nhất
                    ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
                    
                    # Vẽ vòng tròn quanh vật thể được phát hiện
                    # cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                    
                    # Điểm trung tâm của vật thể
                    center = (int(x), int(y))

                    # Vẽ chấm tròn màu đỏ lên bảng vẽ
                    cv2.circle(self.paint_board, center, 5, (0, 0, 255), -1) # Màu đỏ BGR (0,0,255)

            # Kết hợp khung hình camera và bảng vẽ lại với nhau
            # Sử dụng cv2.addWeighted để overlay bảng vẽ lên frame
            final_frame = cv2.addWeighted(frame, 1, self.paint_board, 0.7, 0)


            # Chuyển đổi định dạng để hiển thị trên Tkinter
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    FingerPaintApp(tk.Tk(), " ")