import cv2
import os
import imghdr
import smtplib
import email.message

USERNAME = "kyligalway@gmail.com"
PASSWORD = os.getenv("password")


def send_email(image):
    print("Sending email...")
    cv_image = cv2.imread(image)
    cv2.imshow("Image", cv_image)
    os.getenv("password")
    email_message = email.message.EmailMessage()
    email_message["Subject"] = "Something has entered your camera!"
    email_message.set_content("Someone has entered your camera.")

    with open(image, "rb") as image_file:
        content = image_file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(USERNAME, PASSWORD)
    gmail.sendmail(USERNAME, USERNAME, email_message.as_string())
    gmail.quit()
    print("Email sent.")

