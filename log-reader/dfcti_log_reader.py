#!/usr/bin/env python3


import os
import platform
import numpy as np
from numpy import random as rd
import time
from datetime import datetime
import watchdog

log_file_path = '/var/log/dfcti_cpu_logs.log'


with open(log_file_path, 'r') as opener:
    files = opener.readlines()
    print(files)
