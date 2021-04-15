#!/Users/robertpoenaru/.pyenv/shims/python


import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL

root_email = 'alerts.dfcti@gmail.com'
destination_emails = ['robert.poenaru@outlook.com',
                      'robert.poenaru@gmail.com', 'robert.poenaru@drd.unibuc.ro']

# get the password for the g-mail dev account
password = open('pass.word', 'r').read()


message = MIMEMultipart("alternative")
message["Subject"] = "Alert via DFCTI system"
message["From"] = root_email
message["To"] = ', '.join(destination_emails)


text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""


html = open('message.html', 'r').read()

SEND = True

IN_SEND = True

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
            print('Cannot log-in!')
            print(f'Reason: {exc}')
        else:
            print(f'Successful log-in into -> {root_email}')
            print(f'Sending an e-mail to -> {destination_emails}...✉️')
            for email in destination_emails:
                if(IN_SEND):
                    try:
                        server.sendmail(root_email, email,
                                        message.as_string())
                    except Exception as exc:
                        print(f'Cannot alert send message to {email}...')
                        print(f'Reason: {exc}')
                    else:
                        print(f'Sent message to {email}!')

else:
    print('Not sending e-mails...')
