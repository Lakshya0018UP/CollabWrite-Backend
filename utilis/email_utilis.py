import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

async def send_invite_email_exisiting(to_email:str,head_name:str,invite_link:str):
    subject=f"You have been added to the family plan by {head_name}"
    body=f"""
    <html>
    <body>
        <h2>You have an invitation</h2>
        <p>Click on the following link for to be added into the family</p>
        <p><a href="{invite_link}">Accept Invitation & Sign Up</a></p>
        <p>This link will expire in 72 hours...</p>
    """
    message=MIMEMultipart("alternative")
    message["From"]=GMAIL_EMAIL
    message["To"]=to_email
    message["Subject"]=subject
    message.attach(MIMEText(body,"html"))

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(GMAIL_EMAIL,GMAIL_PASSWORD)
            server.sendmail(GMAIL_EMAIL,to_email,message.as_string())
        return {"status":"success"}
    except Exception as e:
        print(f"Failed to send OTP Email:{e}")
        return {"status":"error","message":str(e)}
    


def send_new_user_invite_link(to_email:str,head_name:str,invite_link:str):
    subject=f"You have been added to the family plan by {head_name}"
    body=f"""
    <html>
    <body>
        <h2>You have an invitation</h2>
        <p>Click on the following link for to be added into the family</p>
        <p><a href="{invite_link}">Accept Invitation & Sign Up</a></p>
        <p>This link will expire in 72 hours...</p>
    """
    message=MIMEMultipart("alternative")
    message["From"]=GMAIL_EMAIL
    message["To"]=to_email
    message["Subject"]=subject
    message.attach(MIMEText(body,"html"))

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(GMAIL_EMAIL,GMAIL_PASSWORD)
            server.sendmail(GMAIL_EMAIL,to_email,message.as_string())
        return {"status":"success"}
    except Exception as e:
        print(f"Failed to send OTP Email:{e}")
        return {"status":"error","message":str(e)}
