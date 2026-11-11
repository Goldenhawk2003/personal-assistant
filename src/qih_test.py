from mail_sender.send_mail import MailSender
import smtplib
from email.message import EmailMessage
import os

import pandas as pd

def read_csv(file_path):
    usecols = ['Contact', 'Location', 'Restrurant']

    df = pd.read_excel(
        file_path,
        sheet_name='Valentines Dinner',
        header=4,
        usecols=usecols
    )

    emails = (
        df['Contact']
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda x: x.str.contains('@', regex=False)]
        .tolist()
    )

    return emails


def send_email(to_email, subject, body):
    
    
    mail_sender = MailSender(sender_email="ammarogeil@gmail.com",
         sender_password=os.environ["JARVIS_GMAIL_APP_PASSWORD"],)
    mail_sender.send_email(to_email, subject, body)

if __name__ == "__main__":
    csv_file_path = r"c:/Users/ammar/Downloads/QueenIsHome.xlsx"
    email_data = read_csv(csv_file_path)
    print(email_data)

    for row in email_data:
        to_email = row
        subject = "Valentine's Day Dinner Inquiry"
        body = body = """Hi there!

            I'm wondering if you guys usually do any Valentine's Day events, like a special menu or anything along those lines.

            Could you please provide me with more details?

            Thank you!
            Ammar Ogeil"""
        send_email(to_email, subject, body)