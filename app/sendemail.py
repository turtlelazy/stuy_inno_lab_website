import os
import smtplib
import imghdr
import datetime as dt
import time
from email.message import EmailMessage


def send(email, text):
    EMAIL_ADDRESS = "testing789project@gmail.com"
    EMAIL_PASSWORD = "jlkcrvpjomtsdkbc"
    contacts = ['testing789project@gmail.com', '22shriya.a@gmail.com']

    msg = EmailMessage()
    msg['Subject'] = 'adi im literally better than you'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    msg.set_content(text)
    # msg.add_alternative("""\
    # <!DOCTYPE html>
    # <html>
    #     <body>
    #         <h1 style="color:SlateGray;">i am amazing i sent this by code muahahahahahah hehehe lols</h1>
    #     </body>
    # </html>
    # """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
