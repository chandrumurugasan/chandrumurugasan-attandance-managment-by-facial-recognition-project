from flask import Flask
from flask_mail import Mail, Message
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import datetime

app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   
# message object mapped to a particular URL ‘/’
@app.route("/Email")
def send_mail(send_from, send_to, subject, text, files=None, server="localhost", port=587, username='chandrumurugasan@gmail.com', password='12072001cS#', isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(fil.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
            msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if isTls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

# Define the sender and recipient email addresses
sender_email = "chandrumurugasan@gmail.com"
recipient_emails = ["reciver1@gmail.com", "reciver2@gmail.com"]

# Define the file path for the attachment
folder_name = "Attendance"
file_name = f"attendance{datetime.date.today().strftime('%m-%d-%y')}"
file_path = os.path.join(folder_name, file_name)

# Define the email subject and body text
email_subject = "Attendance Report"
email_body = "Please find the attendance report attached."

# Call the send_mail function to send the email with the attachment
send_mail(sender_email, recipient_emails, email_subject, email_body, files=[file_path])

if __name__ == '__main__':
   app.run(debug = True)