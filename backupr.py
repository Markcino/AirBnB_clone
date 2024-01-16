#!/usr/bin/env python3
import os
import shutil
import fnmatch
from tqdm import tqdm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

src_file = 'Y:/'
des_path = 'G:/'
ftype = "*.BAK"


def send_success_email():
    subject = "Copying Finished"
    message = "Copying has been completed successfully!"

    msg = MIMEMultipart()
    msg['From'] = os.getenv('FROM_EMAIL')
    msg['To'] = os.getenv('TO_EMAIL')
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('FROM_EMAIL'), os.getenv('EMAIL_PASSWORD'))
    text = msg.as_string()
    server.sendmail(os.getenv('FROM_EMAIL'), os.getenv('TO_EMAIL'), text)
    server.quit()

def send_error_email(error_message):
    subject = "FAIL TO COPY"
    message = f"Failed to Copy Filed, Please Retry Again. Error: {error_message}"

    msg = MIMEMultipart()
    msg['From'] = os.getenv('FROM_EMAIL')
    msg['To'] = os.getenv('TO_EMAIL')
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('FROM_EMAIL'), os.getenv('EMAIL_PASSWORD'))
    text = msg.as_string()
    server.sendmail(os.getenv('FROM_EMAIL'), os.getenv('TO_EMAIL'), text)
    server.quit()

try:
    directories = [dir for dir in os.listdir(src_file) if os.path.isdir(os.path.join(src_file, dir))]

    if not directories:
        raise ValueError("No Most Recent Folder Created, Please Wait!! or Refresh")

    most_recent_dir = max(directories, key=lambda dir: os.path.getctime(os.path.join(src_file, dir)))

    source = os.listdir(os.path.join(src_file, most_recent_dir))
    source = [file for file in source if fnmatch.fnmatch(file, ftype)]

    if not source:
        raise ValueError("No Most Recent File Created, Please Wait!! or Refresh")

    most_recent_file = max(source, key=lambda file: os.path.getctime(os.path.join(src_file, most_recent_dir, file)))

    full_file_name = os.path.join(src_file, most_recent_dir, most_recent_file)

    with tqdm(total=1, desc="Copying files", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as progress_bar:
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, des_path)
            progress_bar.update()

    print("COPYING FINISH.............")
    send_success_email()

except Exception as e:
    print("FAIL TO COPY")
    send_error_email(str(e))