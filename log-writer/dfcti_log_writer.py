#!/usr/bin/env python3


import time
from datetime import datetime

import tqdm  # add a progress bar
import uuid
import os
import platform
import sys  # using it for getting command line arguments
import psutil  # used for getting stats related to the system resources

import numpy as np
from numpy.random import default_rng
rd = default_rng()

now = lambda: float(time.time())
"""Gives the current time"""


log_file_path = '/var/log/dfcti_system_logs.log'


class MachineID:
    """
    Generate a machine ID for the current system.

    When the script is ran for the first time, the presence of a dedicated `MACHINE_ID` file is checked.

    If the file exists, it checks if it is empty or not. If the file is empty, a new machine ID will be generated and stored just ONCE. Otherwise, the already stored machine ID will be used throughout the logging process.

    !It is essential that the machine ID will remain unchanged on the machine!
    """
    machine_id_path = "machine_id"  # !the file will be local relative to the path of the log-writer script itself

    @classmethod
    def Check_File_Exists(self, file_path):
        """
        🔎 📄  Check if the file with machine ID exists or not.
        If the file does not exist, it returns -1.
        """
        try:
            checker = os.path.isfile(file_path)
        except FileNotFoundError as exc:
            print(f'File_Exists_Check_Error: ------> {exc}')
            return False
        else:
            return checker

    @classmethod
    def Check_Empty_File(self, file_path):
        """
        🔎 📄  Check if the file with machine ID is empty.
        This method is called only if the file itself exists in the first place.
        """
        if(MachineID.Check_File_Exists(file_path) == False):
            return -1
        elif(MachineID.Check_File_Exists(file_path) == True):
            try:
                size_check = os.stat(file_path).st_size
            except Exception as exc:
                print(f'File_Size_Check_Error: ----> {exc}')
            else:
                return size_check

    @classmethod
    def Check_Valid_ID(self, file_path):
        """This function checks wether the pre-existing machine ID from the file is indeed a valid UUID4.
        If not, it will return 0.
        """

        file_size = os.stat(file_path).st_size
        if(file_size == 36):
            return 1
        return 0

    @classmethod
    def Generate_Machine_ID(self, file_path):
        """
        💻 Generate a machine ID for the current system.
        If the file is empty, it generates a new machine ID and stores the key there. Otherwise, same ID will be kept.

        Machine ID will not change during multiple runtimes of the logging scripts.
        """
        print('Checking for a Machine-ID...')
        check_exists = MachineID.Check_File_Exists(file_path)
        check_size = MachineID.Check_Empty_File(file_path)
        if(check_exists == False):
            # file does not exist
            # will create machine ID
            # will store ID on the newly created file
            new_machine_id = uuid.uuid4()
            print(' => Creating a new Machine-ID and saving it to file...')
            with open(file_path, 'w') as set_id:
                set_id.write(f'{new_machine_id}')
        else:
            # check if file is empty
            if(MachineID.Check_Valid_ID(file_path)):
                # keep old id
                print('Machine ID already exists -> No new ID required')
                pass
            else:
                # will write an uuid to the file
                print('Generate new Machine ID and saving it to file...')
                new_machine_id = uuid.uuid4()
                with open(file_path, 'w') as set_id:
                    set_id.write(f'{new_machine_id}')

    @classmethod
    def Get_Machine_ID(self):
        MachineID.Generate_Machine_ID(MachineID.machine_id_path)
        with open(MachineID.machine_id_path) as idx:
            ID = idx.read()
        if(ID == '' or ID == ' '):
            return -1
        else:
            return ID


class Random_SystemLogs:
    """Generates any stats related to system logs.
    For example, it can generate CPU usage, disk usage, memory (RAM) usage, and also network usage.
    The generated stats are usually percentages, representing how much of the total allocated resources of that particular machine are being used.
    """
    @ classmethod
    def CPU(self, mean_cpu_usage, usage_spread):
        """Gives the current CPU usage
        This is based on a normal distribution, centered around `mean_cpu_usage`
        The returned values are spreading along accordint to the size of the standard deviation `usage_spread`
        """
        # this is set by the user when running the script
        MEAN_CPU_USAGE = mean_cpu_usage
        # the standard deviation is set by the user when running the script
        STD_DEV = usage_spread

        cpu_usage = lambda: round(rd.normal(MEAN_CPU_USAGE, STD_DEV), 2)
        instant_usage = abs(cpu_usage())
        while(instant_usage > 100):
            instant_usage = abs(cpu_usage())
        return instant_usage

    @ classmethod
    def MEM(self, mean_disk_usage, usage_spread):
        """Gives the current DISK usage
        This is based on a normal distribution, centered around `mean_disk_usage`
        The returned values are spreading along accordint to the size of the standard deviation `usage_spread`
        """
        # this is set by the user when running the script
        MEAN_MEM_USAGE = mean_disk_usage
        # the standard deviation is set by the user when running the script
        STD_DEV = usage_spread

        memory_usage = lambda: round(rd.normal(MEAN_MEM_USAGE, STD_DEV), 2)
        instant_usage = abs(memory_usage())
        while(instant_usage > 100):
            instant_usage = abs(memory_usage())
        return instant_usage


class SystemLogs:
    """Pulls the real system stats of the machine/compute resource on which the script is running
    """
    k_bytes = lambda x: x / 1024.0
    m_bytes = lambda x: x / 1024.0 / 1024.0
    g_bytes = lambda x: x / 1024.0 / 1024.0 / 1024.0

    @classmethod
    def Get_CPU_Usage(cls):
        get_cpu_usage = lambda: psutil.cpu_percent()
        return get_cpu_usage()

    @classmethod
    def Get_MEM_Usage(cls):
        get_mem_usage = lambda: psutil.virtual_memory()[2]
        return get_mem_usage()

    @classmethod
    def Get_Free_Memory(cls):
        get_free_mem = lambda: psutil.virtual_memory()[1]
        return SystemLogs.g_bytes(get_free_mem())


class Write_Logs:
    """
    A set of random system stats which are normally distributed
    Writes logs that are collected from other internal classes within the script
    """

    # the class must take as argument the path to the log file
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    @classmethod
    def Generate_Random_Log_Line(cls, machine_id):
        """
        Will generate a log line with the required information that needs to be monitored
        The system information is randomly generated using a normal distribution
        """

        CPU_MEAN = 70
        CPU_SPREAD = 10
        MEM_MEAN = 70
        MEM_SPREAD = 10

        log_line = f'{datetime.utcnow()} CPU:{Random_SystemLogs.CPU(CPU_MEAN, CPU_SPREAD)}% MEM:{Random_SystemLogs.MEM(MEM_MEAN, MEM_SPREAD)}% MACHINE-ID:{machine_id}'
        return log_line

    @classmethod
    def Generate_System_Log_Line(cls, machine_id):
        """Generates a log line with the system stats
        """
        try:
            log_line = f'{datetime.utcnow()} CPU:{SystemLogs.Get_CPU_Usage()}% MEM:{SystemLogs.Get_MEM_Usage()}% MACHINE-ID:{machine_id}'
        except Exception as exc:
            print(
                f'There was an issue while trying to pull system stats:\nReason: {exc}')
        else:
            return log_line

    @classmethod
    def Write_Log_Line(cls, log_line, log_file_path):
        """
        Once a log line has been generated via the proper method, it writes that line into its corresponding log-file
        """
        try:
            with open(log_file_path, 'a+') as logger:
                logger.write(log_line + '\n')
        except Exception as error:
            print(
                f'There was a problem while trying write logs at -> {log_file_path}\nReason: {error}')
            return 0
        else:
            return 1

    @classmethod
    def Write_Process(cls, total_execution_time, wait_time, log_file_path, machine_id):
        """Starts making log lines
        Each log line is generated after a certain period, given by the user via `wait_time`
        After each line has been successfully generated, it is written in its corresponding log file.
        The process is repeated as long as the runtime is below the total execution time, given through the `execution_time` variable
        The time measurements are given in seconds
        """
        count = 0

        print(f'Starting the log-writing process...')

        start_time = now()
        # https://stackoverflow.com/questions/45808140/using-tqdm-progress-bar-in-a-while-loop
        with tqdm.tqdm(total=total_execution_time) as pbar:
            while(now() - start_time <= total_execution_time):
                try:
                    new_log_line = Write_Logs.Generate_System_Log_Line(
                        machine_id)
                except Exception as exc:
                    print(f'Could not generate log line\nReason: {exc}')
                else:
                    line_wr_proc = Write_Logs.Write_Log_Line(
                        new_log_line, log_file_path)
                    if(line_wr_proc):
                        count += 1
                time.sleep(wait_time)
                pbar.update(wait_time)

        if(os.path.exists(log_file_path) and os.stat(log_file_path).st_size != 0 and count <= total_execution_time):
            """The process is successful only if the log-file does exist, it has non-size, and also the number of events does not succeed the total allowed number (given by the execution time of the process and the system stats pull-rate)
            """
            print(
                f'Finished writing logs successfully at {log_file_path} [Size={round(os.stat(log_file_path).st_size/1024,3)} Kbytes]')
            print(f'{count} log events were registered while pulling system stats.')
        else:
            print(f'Writing process finished unsuccessfully')
            count = -1

        return count


REFRESH_CYCLE = 1
"""
this value represents the frequency for updating the log-file with system information
Example:
`REFRESH_CYCLE=1` means that the log writer will update the file ONCE each second
"""


def Do_Write_Test(machine_id, log_file_path):
    total_execution_time = 69
    try:
        total_execution_time = int(sys.argv[1])
    except IndexError as err:
        print('No argument given!\nDefaulting to the safe value')
    else:
        pass
    proc = Write_Logs.Write_Process(
        total_execution_time, REFRESH_CYCLE, log_file_path, machine_id)


def Do_Write(machine_id, log_file_path):
    total_execution_time = 69
    # initialize the class instance with its corresponding instance variable
    process = Write_Logs(log_file_path)
    try:
        total_execution_time = int(sys.argv[1])
    except IndexError as err:
        print('No argument given!\nDefaulting to the safe value')
    else:
        pass
    process.Write_Process(
        total_execution_time, REFRESH_CYCLE, log_file_path, machine_id)


if __name__ == '__main__':
    MACHINE_ID = MachineID.Get_Machine_ID()
    try:
        Do_Write(MACHINE_ID, log_file_path)
    except KeyboardInterrupt:
        print(f'Finished executing the writing process -> Keyboard Interrupt')
