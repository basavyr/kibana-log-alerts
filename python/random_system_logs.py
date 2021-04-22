#!/Users/robertpoenaru/.pyenv/shims/python


import time
import datetime
import numpy as np
from numpy import random as rd
import emailer as dfcti
import uuid
import matplotlib.pyplot as plt


message = """Hi {name},

You were alerted by the DFCTI monitoring system due to an unexpected issue within the log files that are being watched.
Issue: {alert}


{id}
ID generated at: {time}
https://elk.nipne.ro


This is a test 🥺
"""


DEFAULT_ALERTS = {
    "CPU": "🔥 HIGH CPU USAGE FOR THE PAST 5 MINUTES 🔥",
    "MEM": "🔥 HIGH MEMORY USAGE FOR THE PAST 5 MINUTES 🔥",
    "DISK": "🔥 HIGH DISK MEMORY USAGE FOR THE PAST 5 MINUTES 🔥",
    "NET": "🔥 UNUSUAL NETWORK TRAFFIC FOR THE PAST 5 MINUTES 🔥",
}


time_stamp = lambda: str(datetime.datetime.utcnow())[0:19]
mail_id = lambda: str(uuid.uuid4())


class SystemLogs:

    @classmethod
    def CPU(self):
        """returns the cpu usage as an instant value"""
        MEAN_CPU_USAGE = 45.0
        STD_DEV = 30
        cpu_usage = lambda: round(rd.normal(MEAN_CPU_USAGE, STD_DEV), 2)
        instant_usage = abs(cpu_usage())
        while(instant_usage > 100):
            instant_usage = abs(cpu_usage())
        return instant_usage

    @classmethod
    def MEM(self):
        """returns the memory usage as an instant value"""
        MEAN_MEM_USAGE = 65.0
        STD_DEV = 10
        memory_usage = lambda: round(rd.normal(MEAN_MEM_USAGE, STD_DEV), 2)
        instant_usage = abs(memory_usage())
        while(instant_usage > 100):
            instant_usage = abs(memory_usage())
        return instant_usage

    @classmethod
    def DISK(self):
        """returns the disk usage as an instant value"""
        MEAN_DISK_USAGE = 33.0
        STD_DEV = 20
        disk_usage = lambda: round(rd.normal(MEAN_DISK_USAGE, STD_DEV), 2)
        instant_usage = abs(disk_usage())
        while(instant_usage > 100):
            instant_usage = abs(disk_usage())
        return instant_usage

    @classmethod
    def NET(self):
        """returns the network usage as an instant value"""
        MEAN_NET_USAGE = 25.0
        STD_DEV = 10
        disk_usage = lambda: round(
            rd.normal(MEAN_NET_USAGE, STD_DEV), 2)
        instant_usage = abs(disk_usage())
        while(instant_usage > 100):
            instant_usage = abs(disk_usage())
        return instant_usage


class Watcher:
    @classmethod
    def Monitor_CPU_Usage(self, usage_limit, time_window):
        """
        Constantly watches for CPU usage on the current machine
        In case of high-usage regime, throws an alert

        High-usage regime can be configured by the user
            based on a fixed number of repeated values higher than a certain usage limit 
        """
        refresh_watcher = 2  # cpu info pulls per second
        counter = 0
        Watching = True
        cpu_fail_stack = []
        start_time = time.time()
        while(Watching):
            # cpu_usage = SystemLogs().CPU()
            # # print(cpu_usage)
            # if(cpu_usage > usage_limit):
            #     counter += 1
            #     cpu_fail_stack.append(cpu_usage)
            # else:
            #     counter = 0
            #     cpu_fail_stack.clear()
            #     start_time = time.time()
            # if(counter == repeated_cases and len(cpu_fail_stack) == repeated_cases):
            #     time_elapsed = (time.time() - start_time)
            #     print(
            #         f'🚦 Found anomaly after {time_elapsed} seconds)')
            #     if(time_elapsed >= time_window):
            #         print('Will Alert!')
            #         print(
            #             f'🔥 HIGH CPU USAGE FOR THE PAST {time_window} SECONDS 🔥 ----> {cpu_fail_stack}\nAfter: {time_elapsed}')
            #         start_time = time.time()
            #     else:
            #         print('No Alert Needed!')
            #         print(
            #             f'CPU USAGE WAS HIGH BUT ONLY FOR {time_elapsed} SECONDS ----> {cpu_fail_stack}')
            #     counter = 0
            #     cpu_fail_stack.clear()
            time.sleep(1 / refresh_watcher)
            print(time.time() - start_time)
            start_time = time.time()
            time.sleep(1 / refresh_watcher)
            print(time.time() - start_time)

    @classmethod
    def MeasureTime(self, time_window, time_steps):
        frequency = 1 / time_steps
        counter = 0
        start_time = time.time()
        while(True):
            counter += 1
            time.sleep(frequency)
            elapsed_time = time.time() - start_time
            print(counter)
            # if(elapsed_time >= time_window):
            #     print(f'{time_window} seconds passed...')
            #     print(f'counter value: {counter}')
            #     if(counter == time_window * time_steps):
            #         print('counter is ok')
            #     counter = 0
            #     start_time = time.time()


Watcher.MeasureTime(10,22)
# Watcher().Monitor_CPU_Usage(45, 5)


# CPU_USAGES = [SystemLogs.CPU() for _ in range(10000)]
# MEM_USAGES = [SystemLogs.MEM() for _ in range(10000)]
# DISK_USAGES = [SystemLogs.DISK() for _ in range(10000)]
# NET_USAGES = [SystemLogs.NET() for _ in range(10000)]
# fig, ax = plt.subplots(4, 1, sharex=True)
# ax[0].hist(CPU_USAGES, bins=50)
# ax[1].hist(MEM_USAGES, bins=50)
# ax[2].hist(DISK_USAGES, bins=50)
# ax[3].hist(NET_USAGES, bins=50)
# plt.show()
custom_message = lambda client_name, c_time, mailID, alert: message.format(
    name=f'{client_name}', time=f'{c_time}', id=f'Message ID: #{mailID}', alert=f'{alert}')


def Log_Emails(client, alert, send_state):
    LOG_FILE = 'email-logs.log'
    current_mail_id = mail_id()
    current_time_stamp = time_stamp()
    message = custom_message(
        client, current_time_stamp, current_mail_id, alert)
    try:
        dfcti.Send_TEXT_Email(dfcti.EMAIL_LIST, message, send_state)
    except Exception as exc:
        print('There was a problem sending the alert...')
        print(f'Reason: {exc}')
    else:
        if(send_state):
            with open(LOG_FILE, 'a+') as logger:
                logger.write(
                    f'Time: {current_time_stamp} Mail_ID: {current_mail_id} Client_ID: {client}\n')


Log_Emails('Robert', DEFAULT_ALERTS["CPU"], 0)
