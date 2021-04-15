#!/Users/robertpoenaru/.pyenv/shims/python


import smtplib
import ssl

port = 465  # For SSL


email = 'alerts.dfcti@gmail.com'
password = open('pass.word', 'r').read()

destination = 'robert.poenaru@outlook.com'

message = """\
Subject: Hi there

This message is sent from Python."""


# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    try:
        server.login(email, password)
    except:
        print('Error logging in')
    else:
        print(f'Successful log-in into -> {email}')
        print(f'Sending an e-mail to -> {destination}...✉️')
        server.sendmail(email, destination, message)
