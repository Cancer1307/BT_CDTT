import cv2
import time


# Khởi tạo webcam
cap = cv2.VideoCapture(0)

# Đặt kích thước khung hình
cap.set(3, 640)
cap.set(4, 480)

# Lưu trữ 3 khung hình để so sánh
frame1 = None
frame2 = None
frame3 = None

while True:
    # Đọc khung hình
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(2000)  # chờ 2 giây trước khi chụp ảnh tiếp theo

    # Lưu khung hình mới nhất
    frame1 = frame2
    frame2 = frame3
    frame3 = frame

    # Nếu đã có đủ 3 khung hình thì bắt đầu so sánh
    if frame1 is not None and frame2 is not None and frame3 is not None:
        # Chuyển sang ảnh xám và giảm nhiễu
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

        blur1 = cv2.GaussianBlur(gray1, (21, 21), 0)
        blur2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        blur3 = cv2.GaussianBlur(gray3, (21, 21), 0)

        # Tính toán sự khác biệt giữa 3 ảnh
        diff1 = cv2.absdiff(blur1, blur2)
        diff2 = cv2.absdiff(blur2, blur3)

        # So sánh sự khác biệt giữa 3 ảnh
        thresh = cv2.threshold(cv2.bitwise_and(diff1, diff2), 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Hiển thị ảnh kết quả
        cv2.imshow('Frame', frame3)
        cv2.imshow('Thresh', thresh)

        # Nếu phát hiện sự khác biệt lớn thì đó là xe vi phạm
        if cv2.countNonZero(thresh) > 5000:
            print('Xe vi phạm')

    # Đợi 1 phút trước khi chụp ảnh tiếp theo
    time.sleep(60)
    # Nếu nhấn phím 'q' thì thoát chương trình
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng các tài nguyên
cap.release()
cv2.destroyAllWindows()