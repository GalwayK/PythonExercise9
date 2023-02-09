import glob
import os

import cv2
import numpy
import time
import emailing
from threading import Thread


def clean_folder():
    print("Cleaning folder.")
    status_list.clear()
    files = glob.glob("files/images/*.png")
    for file in files:
        os.remove(file)
    print("Folder cleaned.")

video = cv2.VideoCapture(0)

time.sleep(0.016)
first_frame = None
status_list = []
count = 0
while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    cv2.imshow("My video", gray_frame_gau)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("Delta Frame", delta)

    thresh = cv2.threshold(delta, 50, 255, cv2.THRESH_BINARY)[1]
    dilute = cv2.dilate(thresh, None, iterations=2)
    cv2.imshow("Thresh Frame", dilute)

    contours, check = cv2.findContours(dilute, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
        if rectangle.any():
            status = 1
            cv2.imwrite(f"files/images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("files/images/*.png")

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=emailing.send_email,
                              args=(f"files/images/{int(count / 2)}.png", ))
        email_thread.daemon = True

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()


        count = 0

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    try:
        clean_thread.start()
    except:
        pass
video.release()

# cv2 uses BGR instead of RGB
# a = numpy.array([
#     [[255, 0, 0],
#      [255, 255, 255],
#      [255, 255, 255],
#      [187, 41, 160]],
#     [[255, 255, 255],
#      [255, 255, 255],
#      [255, 255, 255],
#      [255, 255, 255]],
#     [[255, 255, 255],
#      [0, 0, 0],
#      [47, 255, 173],
#      [255, 255, 255]]
# ])
#
# array = cv2.imwrite("files/images/image_two.png", a)
#
# print(array)


# check, frame = video.read()
# time.sleep(1)
# check2, frame2 = video.read()
# time.sleep(1)
# check3, frame3 = video.read()
#
# print(check)
# print(frame)
# print(frame2)
# print(frame3)
#
# cv2.imwrite(f"files/images/frame.png", frame)
# cv2.imwrite(f"files/images/frame2.png", frame2)
# cv2.imwrite(f"files/images/frame3.png", frame3)
