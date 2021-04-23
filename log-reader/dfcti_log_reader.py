#!/usr/bin/env python3


import os
import platform
import numpy as np
from numpy import random as rd
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

log_file_path = '/var/log/dfcti_cpu_logs.log'


class Modified_State_Handler(FileSystemEventHandler):
    def on_modified(self, event):
        event_path = event.src_path
        if(event_path == '/private' + log_file_path):
            with open(log_file_path, 'r') as reader:
                last_line = reader.readlines()
                try:
                    # must append only the value of the cpu or memory
                    stored_values.append(last_line[len(last_line) - 1])
                except Exception as error:
                    print(f'could not write into the array')
                    print(f'Reason -> {error}')
                else:
                    pass


class Reader():
    get_cpu_usage = lambda log_line: log_line[log_line.find(
        'CPU:') + len('CPU:'):log_line.find('%', log_line.find(
            'CPU:'))]

    get_mem_usage = lambda log_line: log_line[log_line.find(
        'MEM:') + len('MEM:'):log_line.find('%', log_line.find(
            'MEM:'))]

    @classmethod
    def Watch_Log_File(self, log_file, execution_time):

        event_handler = Modified_State_Handler()

        observer = Observer()
        observer.schedule(event_handler, path=log_file, recursive=False)
        observer.start()

        count = 0
        watch_state = True

        total_execution_time = time.time()
        while(watch_state):
            # count the stack before updating it
            current_stack_length_0 = len(stored_values)

            # stop if the total execution time has passed
            # stop if no new entries are coming into the stored values
            if(time.time() - total_execution_time >= execution_time):
                print(f'finished watching the log file')
                watch_state = False
                return

            print(stored_values)
            time.sleep(1)

            # count the stack after updating it
            current_stack_length_1 = len(stored_values)

            print(stored_values)

            if(current_stack_length_0 == current_stack_length_1):
                count += 1
            else:
                count = 0
            if(count == 5):  # stop if the log stream hangs up
                print('No incoming logs...')
                print('Stopping the watcher')
                watch_state = False
                return

        observer.stop()
        observer.join()


# stored_values = []
# Reader.Watch_Log_File(log_file_path, 1000)
