import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp

class FingerPaintApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Mở camera
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        self.canvas_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.canvas_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Bảng vẽ
        self.paint_board = np.zeros((self.canvas_height, self.canvas_width, 3), np.uint8)

        # Cấu hình MediaPipe
        try:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
        except AttributeError:
            print("Lỗi: Không tìm thấy 'mediapipe.solutions'. Hãy thử cài lại bằng: pip install mediapipe")
            return

        self.delay = 10
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Lấy điểm số 8 (đầu ngón trỏ)
                    tip = hand_landmarks.landmark[8]
                    cx, cy = int(tip.x * self.canvas_width), int(tip.y * self.canvas_height)
                    
                    # Vẽ màu đỏ lên bảng vẽ
                    cv2.circle(self.paint_board, (cx, cy), 10, (0, 0, 255), -1)

            # Gộp hình vẽ vào camera
            gray = cv2.cvtColor(self.paint_board, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            frame[mask > 0] = self.paint_board[mask > 0]

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

if __name__ == "__main__":
    FingerPaintApp(tk.Tk(), "App Vẽ Bằng Ngón Tay")