import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Mở nguồn video (camera mặc định là 0)
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        # Tạo Canvas để hiển thị video
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Nút Chụp ảnh
        self.btn_snapshot = tk.Button(window, text="Chụp ảnh và Lưu", width=20, 
                                     command=self.snapshot, bg="#4CAF50", fg="white")
        self.btn_snapshot.pack(padx=10, pady=10)

        # Tạo thư mục lưu ảnh nếu chưa có
        if not os.path.exists("captured_images"):
            os.makedirs("captured_images")

        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Đọc khung hình hiện tại từ camera
        ret, frame = self.vid.read()
        if ret:
            # Lưu ảnh vào thư mục mẫu
            filename = "captured_images/photo.jpg"
            cv2.imwrite(filename, frame)
            print(f"Đã lưu ảnh tại: {filename}")
            
            # Hiệu ứng thông báo nhỏ trên console
            self.show_save_notification()

    def update(self):
        # Lấy khung hình từ camera
        ret, frame = self.vid.read()
        if ret:
            # Chuyển đổi định dạng màu từ BGR sang RGB để Tkinter hiểu được
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def show_save_notification(self):
        # Có thể thêm logic hiển thị popup ở đây
        pass

    def __del__(self):
        # Giải phóng camera khi đóng ứng dụng
        if self.vid.isOpened():
            self.vid.release()

# Khởi chạy ứng dụng
if __name__ == "__main__":
    CameraApp(tk.Tk(), "Python Camera - Chụp ảnh")