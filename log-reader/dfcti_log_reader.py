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
                stored_values.append(last_line[len(last_line) - 1])


event_handler = Modified_State_Handler()
observer = Observer()
observer.schedule(event_handler, path=log_file_path, recursive=False)


stored_values = []
observer.start()
while(True):
    time.sleep(5)
    print(stored_values)
    stored_values.clear()
observer.stop()
observer.join()
