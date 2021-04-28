#!/usr/bin/env python3


import os
import platform
import numpy as np
from numpy.random import default_rng
import time
from datetime import datetime
import uuid

rd = default_rng()


log_file_path = '/var/log/dfcti_system_logs.log'


class MachineID:
    """
    Generate a machine ID for the current system.

    When the script is ran for the first time, the presence of a dedicated `MACHINE_ID` file is checked.

    If the file exists, it checks if it is empty or not. If the file is empty, a new machine ID will be generated and stored just ONCE. If the file is not empty, then the already stored machine ID will be used throughout the logging process.

    It is essential that the machine ID will remain unchanged on the machine.
    """
    machine_id_path = "machine_id"

    @classmethod
    def Check_File_Exists(self, file_path):
        """
        🔎 📄  Check if the file with machine id exists or not
        """
        try:
            checker = os.path.isfile(file_path)
        except FileNotFoundError as exc:
            print(f'File_Exists_Error: ------> {exc}')
            return -1
        else:
            return checker

    @classmethod
    def Check_Empty_File(self, file_path):
        """
        🔎 📄  Check if the file with machine id exists or not
        """
        if(MachineID.Check_File_Exists(file_path) == False):
            return -1
        elif(MachineID.Check_File_Exists(file_path) == True):
            try:
                size_check = os.stat(file_path).st_size
            except Exception as exc:
                print(f'Size_Check_Error: ----> {exc}')
            else:
                return size_check

    @classmethod
    def Generate_Machine_ID(self):
        """
        💻 Generate a machine ID for the current system.
        """
        check_exists = MachineID.Check_File_Exists(MachineID.machine_id_path)
        check_size = MachineID.Check_Empty_File(MachineID.machine_id_path)
        if(check_exists == False):
            # file does not exist
            new_machine_id = uuid.uuid4()
            with open(MachineID.machine_id_path, 'w+') as set_id:
                set_id.write(f'{new_machine_id}')
        else:
            # check if file is empty
            if(check_size != 0):
                # keep old id
                pass
            else:
                # will write an uuid to the file
                new_machine_id = uuid.uuid4()
                with open(MachineID.machine_id_path, 'w+') as set_id:
                    set_id.write(f'{new_machine_id}')

    @classmethod
    def Get_Machine_ID(self):
        MachineID.Generate_Machine_ID()
        with open(MachineID.machine_id_path) as idx:
            ID = idx.read()
        return ID


MACHINE_ID = MachineID.Get_Machine_ID()


class SystemLogs:
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


class Write_Logs:
    """
    Writes logs that are collected from other internal classes within the script
    """

    @ classmethod
    def Generate_Log_Line(self):
        """
        Will generate a log line with the required information that needs to be monitored
        """

        CPU_MEAN = 70
        CPU_SPREAD = 10
        MEM_MEAN = 70
        MEM_SPREAD = 10

        log_line = f'{datetime.utcnow()} CPU:{SystemLogs().CPU(CPU_MEAN, CPU_SPREAD)}% MEM:{SystemLogs().MEM(MEM_MEAN, MEM_SPREAD)}% MACHINE-ID:{MACHINE_ID}'
        return log_line

    @ classmethod
    def Write_Log_Line(self, log_line, log_file):
        """
        Once a log line has been generated via the proper method, it writes that line into its corresponding log-file
        """
        try:
            with open(log_file, 'a+') as logger:
                logger.write(log_line + '\n')
        except Exception as error:
            print(
                f'There was a problem while trying write logs\nReason: {error}')
        else:
            pass

    @ classmethod
    def Write_Process(self, execution_time_secs, wait_time):
        """Starts making log lines
        Each log line is generated after a certain period, given by the user via `wait_time`
        After each line has been successfully generated, it is written in its corresponding log file.
        The process is repeated as long as the runtime is below the total execution time, given through the `execution_time` variable
        The time measurements are given in seconds (sec,s,secs)
        """
        writing_state = True
        total_execution_time = time.time()
        while(writing_state):
            if(time.time() - total_execution_time >= execution_time_secs):
                print('Total executime time reached.\nStopping the writing process...')
                break
            print(f'Generating log line...')
            try:
                new_log_line = Write_Logs().Generate_Log_Line()
            except Exception as exc:
                print(f'Could not generate log line\nReason: {exc}')
            else:
                print(f'Writing log line at {log_file_path}')
                try:
                    Write_Logs().Write_Log_Line(new_log_line, log_file_path)
                except Exception as exc:
                    print(f'Could not write the log line\nReason: {exc}')
                else:
                    pass
            time.sleep(wait_time)


Write_Logs.Write_Process(60, 1)
