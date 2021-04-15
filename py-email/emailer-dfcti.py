#!/Users/robertpoenaru/.pyenv/shims/python


import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime


def Get_Email_List(email_list):
    EMAIL_LIST = []
    return EMAIL_LIST


def Get_Message(html_file):
    HTML_CONTENT = open(html_file, 'r').read()
    return HTML_CONTENT


def Send_Email(email_list, email_content, alert_state):
    PORT = 465  # For SSL
    ROOT_EMAIL = 'alerts.dfcti@gmail.com'

    # get the password for the g-mail dev account
    PASSWORD = open('pass.word', 'r').read()

    message = MIMEMultipart("alternative")
    message["Subject"] = f'{datetime.datetime.utcnow()} - Alert via DFCTI monitoring system'
    message["From"] = ROOT_EMAIL

    # https://stackoverflow.com/questions/38151440/can-anyone-tell-my-why-im-getting-the-error-attributeerror-list-object-has
    message["To"] = ', '.join(email_list)

    IN_SEND = False

    if(alert_state == True):
        print('Alert service started...⚙️')
        if(len(email_list) == 0):
            print('No clients to alert...')
            return
        HTML_MESSAGE = MIMEText(email_content, "html")

        message.attach(HTML_MESSAGE)

        # Create a secure SSL context
        CONTEXT = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=CONTEXT) as MAIL_SERVER:
            try:
                MAIL_SERVER.login(ROOT_EMAIL, PASSWORD)
            except Exception as exc:
                print(f'❌ Cannot log-in!')
                print(f'Reason: {exc}')
            else:
                print(f'✅ Successful log-in into -> {ROOT_EMAIL}')
                print(f'⚙️ Ready to send alerts to -> {email_list}')
                for email in email_list:
                    if(IN_SEND):
                        try:
                            MAIL_SERVER.sendmail(ROOT_EMAIL, email,
                                                 message.as_string())
                        except Exception as exc:
                            print(f'❌ Cannot send alert to {email}...')
                            print(f'Reason: {exc}')
                        else:
                            print(f'📤 Sent alert to {email}! ✅')
    else:
        print('Not sending any alerts...')


html_content = Get_Message('message.html')
Send_Email(['robert.poenaru@outlook.com'], html_content, True)
Send_Email([], html_content, True)
