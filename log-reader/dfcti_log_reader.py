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
                content = reader.readlines()
                last_line = content[-1]
                try:
                    # must append only the value of the cpu or memory
                    cpu_stack.append(Reader.get_cpu_usage(last_line))
                except Exception as error:
                    print(f'could not add CPU stats into the cpu stack')
                    print(f'Reason -> {error}')
                else:
                    pass
                try:
                    # must append only the value of the cpu or memory
                    mem_stack.append(Reader.get_mem_usage(last_line))
                except Exception as error:
                    print(f'could not add MEM stats into the cpu stack')
                    print(f'Reason -> {error}')
                else:
                    pass
                try:
                    machine_id = Reader.get_machine_id(last_line)
                except Exception as error:
                    print(f'could not get machine ID')
                    print(f'Reason -> {error}')
                else:
                    pass


class Reader():
    get_cpu_usage = lambda log_line: float(log_line[log_line.find(
        'CPU:') + len('CPU:'):log_line.find('%', log_line.find(
            'CPU:'))])

    get_mem_usage = lambda log_line: float(log_line[log_line.find(
        'MEM:') + len('MEM:'):log_line.find('%', log_line.find(
            'MEM:'))])

    get_machine_id = lambda log_line: str(
        log_line[log_line.find('MACHINE-ID:') + len('MACHINE-ID:'):])

    @ classmethod
    def Watch_Log_File(self, log_file, execution_time):

        event_handler = Modified_State_Handler()

        observer = Observer()
        observer.schedule(event_handler, path=log_file, recursive=False)
        observer.start()

        count = 0
        watch_state = True

        total_execution_time = time.time()
        while(watch_state):
            # count the stacks before updating it
            cpu_stack_length_0 = len(cpu_stack)
            mem_stack_length_0 = len(mem_stack)

            # stop if the total execution time has passed
            # stop if no new entries are coming into the stored values
            if(time.time() - total_execution_time >= execution_time):
                print(f'finished watching the log file')
                watch_state = False
                return

            time.sleep(1)

            # count the stacks after updating it
            cpu_stack_length_1 = len(cpu_stack)
            mem_stack_length_1 = len(mem_stack)

            if((cpu_stack_length_0 == cpu_stack_length_1) or (mem_stack_length_0 == mem_stack_length_1)):
                count += 1
            else:
                count = 0
            if(count == 5):  # stop if the log stream hangs up
                print('No incoming logs...')
                print('Stopping the watcher')
                watch_state = False
                print('CPU stack:')
                print(cpu_stack)
                print('Memory stack:')
                print(mem_stack)
                print('Machine ID')
                print(machine_id)
                return

        observer.stop()


cpu_stack = []
mem_stack = []
machine_id = ''
Reader.Watch_Log_File(log_file_path, 1000)

string = '2021-04-23 13:54:16.092620 CPU:74.08% MEM:52.45% MACHINE-ID:8273d378-9b1e-4281-a673-9421bde36c79'

# print(string[string.find('MACHINE-ID:') + len('MACHINE-ID:'):])

# print(Reader.get_machine_id(string))
