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


k_bytes = lambda value: value / 1024.
m_bytes = lambda value: value / 1024. / 1024.
g_bytes = lambda value: value / 1024. / 1024. / 1024.


def Get_Network_Usage():
    TIME_WINDOW = 1
    inf = "en0"
    net = lambda: psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in1 = net().bytes_recv
    net_out1 = net().bytes_sent
    time.sleep(TIME_WINDOW)
    net_in2 = net().bytes_recv
    net_out2 = net().bytes_sent
    traffic = ["in:", k_bytes((net_in2 - net_in1) / TIME_WINDOW), "out:",
               k_bytes((net_out2 - net_out1) / TIME_WINDOW)]
    return(traffic)


def Get_CPU_Usage():
    cpu_usage = lambda: psutil.cpu_percent()
    return(cpu_usage())


def Get_Disk_Usage():
    partition = '/System/Volumes/Data'
    du = lambda: psutil.disk_usage(partition).percent
    # du = lambda: psutil.disk_partitions()
    # for du_item in du():
        # print(du_item)
    print(du())
    # return(du())


def Get_Memory_Usage():
    mu_percentage = lambda: psutil.virtual_memory()[2]
    return(mu_percentage())


def Log_Line():
    CPU = Get_CPU_Usage()
    MEMORY = Get_Memory_Usage()
    DISK = Get_Disk_Usage()
    NETWORK = Get_Network_Usage()
    TIME_STAMP = datetime.utcnow()
    UUID = uuid.uuid4()
    SYSTEM = f'{platform.processor()}-{platform.architecture()[0]}'
    log_line = f'{TIME_STAMP} cpu:{CPU}% mem:{MEMORY}% disk_usage:{DISK}% net_in:{NETWORK[1]}KB/s net_out:{NETWORK[3]}KB/s sys:{SYSTEM}'
    print(log_line)
    time.sleep(1)


Get_Disk_Usage()

# while(True):
#     Log_Line()

# print(psutil.virtual_memory()[0] / 1024. / 1024. / 1024.)
# print(psutil.virtual_memory()[1] / 1024. / 1024. / 1024.)

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
