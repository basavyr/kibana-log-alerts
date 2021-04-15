#!/Users/robertpoenaru/.pyenv/shims/python


import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL

root_email = 'alerts.dfcti@gmail.com'
destination_email = 'robert.poenaru@outlook.com'

# get the password for the g-mail dev account
password = open('pass.word', 'r').read()


message = MIMEMultipart("alternative")
message["Subject"] = "Alert via DFCTI system"
message["From"] = root_email
message["To"] = destination_email


text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""


html = open('message.html', 'r').read()
print(html)

SEND = True


if(SEND):
    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    html_message = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(html_message)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login(root_email, password)
        except Exception as exc:
            print('Error logging in!')
            print(f'Error: {exc}')
        else:
            print(f'Successful log-in into -> {root_email}')
            print(f'Sending an e-mail to -> {destination_email}...✉️')
            server.sendmail(root_email, destination_email, message.as_string())
else:
    print('Not sending e-mails...')
