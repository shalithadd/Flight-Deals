import os
from smtplib import SMTP
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv('.env')


class NotificationManager:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_SID')
        self.auth_token = os.getenv('TWILIO_TOKEN')
        self.from_number = os.getenv('FROM_NUMBER')
        self.to_number = os.getenv('TO_NUMBER')
        self.my_email = os.getenv('MY_EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')

    def send_message(self, data):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            body=data,
            from_=self.from_number,
            to=self.to_number
        )
        print(message.status)

    def send_email(self, message, email, name):
        with SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(
                from_addr=self.my_email,
                to_addrs=email,
                msg=f"Subject: Low Price Alert!\n\nHello {name},\n{message}".encode('utf-8'),
            )
