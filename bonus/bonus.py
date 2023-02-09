import streamlit
import cv2
import time
import datetime

streamlit.title("Webcam Detection App")
webcam_open = streamlit.button("Open Webcam")

if webcam_open:
    streamlit.subheader("Showing webcam")
    streamlit_image = streamlit.image([])
    video = cv2.VideoCapture(0)
    time.sleep(.016)
    while True:

        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        date_now = datetime.datetime.now().strftime("%A, %B %Y")
        time_now = datetime.datetime.now().strftime("%H:%M:%S %p")

        cv2.putText(img=frame, text=date_now, org=(50, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(255, 255, 255),
                    thickness=1, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=time_now, org=(50, 85),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(255, 20, 20),
                    thickness=1, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)

