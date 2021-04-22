#!/Users/robertpoenaru/.pyenv/shims/python

import time
import datetime
from random import random as rd
import emailer as dfcti
import uuid


time_stamp = lambda: str(datetime.datetime.utcnow())[0:19]
mail_id = lambda: str(uuid.uuid4())
message = """Hi {name}
This is a test 🥺
Issue: {alert}




{id}
ID generated at: {time}
https://elk.nipne.ro
"""


custom_message = lambda client_name, c_time, mailID, alert: message.format(
    name=f'{client_name}', time=f'{c_time}', id=f'Message ID: #{mailID}', alert=f'{alert}')


def Log_Emails(client, alert):
    LOG_FILE = 'email-logs.log'
    current_mail_id = mail_id()
    current_time_stamp = time_stamp()
    message = custom_message(
        client, current_time_stamp, current_mail_id, alert)
    try:
        dfcti.Send_TEXT_Email(dfcti.EMAIL_LIST, message, True)
    except Exception as exc:
        print('There was a problem sending the alert...')
        print(f'Reason: {exc}')
    else:
        with open(LOG_FILE, 'a+') as logger:
            logger.write(
                f'Time: {current_time_stamp} Mail_ID: {current_mail_id} Client_ID: {client}\n')


Log_Emails('Robert', '🔥 CPU_USAGE 🔥')
