import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def send_password_reset_email(username, link, receiver_email):
    
    # Create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Start TLS for security
    s.starttls()
    
    # Authentication
    s.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
    
    # Create a MIMEText message object
    msg = MIMEMultipart("alternative")
    msg['From'] = os.getenv("MAIL_USERNAME")
    msg['To'] = receiver_email
    msg['Subject'] = "Password Reset Request"
    
    # Define your HTML message
    html_message = f'''
    <html>
    <head></head>
    <body>
        <p>Dear {username},</p>
        <p>You requested to reset your password. Please click on the following link to reset your password:</p>
        <p><a href={link}>Reset Password Link</a></p>
        <p>If you did not make this request, please ignore this email and no changes will be made.</p>
        <br>
        <p>Best regards.</p>
    </body>
    </html>
    '''
    
    # Attach the HTML message
    msg.attach(MIMEText(html_message, "html"))
    
    # Sending the email
    s.sendmail(os.getenv("MAIL_USERNAME"), receiver_email, msg.as_string())
    
    # Terminating the session
    s.quit()
