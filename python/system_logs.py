#!/usr/bin/env python3

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
    # show the network information for the entire interface group
    net = lambda: psutil.net_io_counters(pernic=False, nowrap=True)
    net_in1 = net().bytes_recv
    net_out1 = net().bytes_sent
    time.sleep(TIME_WINDOW)
    net_in2 = net().bytes_recv
    net_out2 = net().bytes_sent
    traffic = list(map(k_bytes, [
                   (net_in2 - net_in1) / TIME_WINDOW, (net_out2 - net_out1) / TIME_WINDOW]))
    return(f'network_in:{traffic[0]}KB/s network_out:{traffic[1]}KB/s')


def Get_CPU_Usage():
    cpu_usage = lambda: psutil.cpu_percent()
    return(cpu_usage())


def Get_Disk_Usage():
    # get the partitions of the current system
    """ !!! Tested only on MacOS
    """
    # partitions = [partition[1] for partition in psutil.disk_partitions()]
    # partition = partitions[0]
    # du = lambda partition: psutil.disk_usage(partition)

    # get disk info
    disk_io_info = lambda: psutil.disk_io_counters(perdisk=False, nowrap=True)

    disk_io_read_1 = disk_io_info().read_bytes
    disk_io_write_1 = disk_io_info().write_bytes
    time.sleep(1)
    disk_io_read_2 = disk_io_info().read_bytes
    disk_io_write_2 = disk_io_info().write_bytes

    disk_io_read = disk_io_read_2 - disk_io_read_1
    disk_io_write = disk_io_write_2 - disk_io_write_1

    disk_io = list(map(k_bytes, [disk_io_write, disk_io_read]))
    return(f'disk_write:{disk_io[0]}KB/s disk_read:{disk_io[1]}KB/s')


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
    log_line = f'{TIME_STAMP} cpu:{CPU}% mem:{MEMORY}% {DISK} {NETWORK} sys:{SYSTEM}'
    return(log_line)


while(True):
    #     Log_Line()
    print(Get_Network_Usage())


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
