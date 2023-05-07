import tkinter as tk
import cv2
import time
import numpy as np
import tensorflow as tf
import threading

class ParkingDetectionSystem:
    def __init__(self, master):
        self.master = master
        master.title("Hệ thống báo đậu xe trái phép")

        # khởi tạo các biến và đối tượng
        self.is_running = False
        self.model = tf.keras.models.load_model('path/to/model')
        self.cap = cv2.VideoCapture(0)
        self.recorded_violations = []

        # thiết lập các đối tượng GUI
        self.title_label = tk.Label(master, text="Hệ thống báo đậu xe trái phép", font=("Helvetica", 20))
        self.start_button = tk.Button(master, text="Bắt đầu", command=self.start)
        self.stop_button = tk.Button(master, text="Dừng lại", command=self.stop)
        self.violations_button = tk.Button(master, text="Xem thông tin xe vi phạm", command=self.show_violations)
        self.status_label = tk.Label(master, text="Hệ thống đang chưa chạy", font=("Helvetica", 14), fg="red")

        # đặt các đối tượng GUI vào cửa sổ
        self.title_label.grid(row=0, column=0, columnspan=2)
        self.start_button.grid(row=1, column=0)
        self.stop_button.grid(row=1, column=1)
        self.violations_button.grid(row=2, column=0, columnspan=2)
        self.status_label.grid(row=3, column=0, columnspan=2)

    def start(self):
        self.is_running = True
        self.status_label.config(text="Hệ thống đang chạy", fg="green")

        while self.is_running:
            ret, frame1 = self.cap.read()
            time.sleep(60) # wait for 1 minute before capturing the next frame
            ret, frame2 = self.cap.read()
            time.sleep(60) # wait for 1 minute before capturing the next frame
            ret, frame3 = self.cap.read()
    
            # preprocess frames
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1 = cv2.resize(frame1, (224, 224))
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            frame2 = cv2.resize(frame2, (224, 224))
            frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
            frame3 = cv2.resize(frame3, (224, 224))
    
            # combine frames
            frames = np.array([frame1, frame2, frame3])
    
            # make predictions
            predictions = self.model.predict(frames)
    
            # check if car is detected in any of the frames
            if np.any(predictions > 0.5):
                print("Car parked illegally detected!")
                self.recorded_violations.append(time.strftime("%Y-%m-%d %H:%M:%S"))

 frame3 = cv2.putText(frame3, "Hệ thống đang chạy", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame',frame3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    self.cap.release()
    cv2.destroyAllWindows()
def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.detect_parking_violation)
        self.thread.start()

    def stop(self):
        self.is_running = False

    def view_violations(self):
        print("Thông tin vi phạm:")
        for violation in self.recorded_violations:
            print(violation)
# main program
detection_system = ParkingDetectionSystem()

while True:
    print("1. Bắt đầu")
    print("2. Dừng lại")
    print("3. Xem thông tin vi phạm")
    print("4. Thoát")

    choice = input("Lựa chọn của bạn: ")
 if choice == "1":
        detection_system.start()
    elif choice == "2":
        detection_system.stop()
        detection_system.thread.join()
    elif choice == "3":
        detection_system.view_violations()
    elif choice == "4":
        break
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
