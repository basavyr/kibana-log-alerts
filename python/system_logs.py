#!/Users/robertpoenaru/.pyenv/shims/python
#!/usr/bin/python3

import numpy as np
import numpy.random as rd
import time
from datetime import datetime
import os
import platform
import psutil
import uuid


log_file = '/tmp/system_info_pysym.log'
test_file = 'system_info_pysym.log'


def Get_Network_Usage(interval):
    TIME_WINDOW = interval
    inf = "en0"
    gbytes = lambda value: value / 1024.
    net = lambda: psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in1 = net().bytes_recv
    net_out1 = net().bytes_sent
    time.sleep(TIME_WINDOW)
    net_in2 = net().bytes_recv
    net_out2 = net().bytes_sent
    traffic = [(net_in2 - net_in1) / TIME_WINDOW,
               (net_out2 - net_out1) / TIME_WINDOW]
    print(list(map(gbytes, traffic)))


while(True):
    Get_Network_Usage(5)

# print(psutil.virtual_memory()[0] / 1024. / 1024. / 1024.)
# print(psutil.virtual_memory()[1] / 1024. / 1024. / 1024.)

# print(psutil.cpu_percent())

# for _ in range(5):
#     counter = 1
#     with open(test_file, 'a+') as logger:
#         print('Writing logs...')
#         CPU = platform.processor()
#         ARCH = platform.architecture()
#         # INFO = platform.uname()
#         TIME = datetime.utcnow()
#         ID = uuid.uuid4()
#         TODAY = f'{TIME.day}-{TIME.month}'
#         logger.write(f'{TIME} {TODAY}-{counter} {CPU}-{ARCH[0]}\n')
#         time.sleep(2)
#     counter += 1
