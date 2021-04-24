#!/usr/bin/env python3


import os
import platform
import numpy as np
from numpy import random as rd
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Set the path to the log file used for analysis
log_file_path = '/var/log/dfcti_system_logs.log'


class Attachment:
    @classmethod
    def Create_Attachment(data, file_path):
        content = f'This is an attachment\n{data}\nPath to file: {file_path}'
        return content


class Message:
    @classmethod
    def Create_Message(self, name, info, stats):
        message = """
        Hey {name},
        You have received this message because you are on the DevOps list managing the computing resources at DFCTI.

        There are issues with one of the machines. Please take care.
        More info: {info}
        Stats: {stats}

        The DFCTI Team,
        https://elk.nipne.ro
        """
        return message.format(name=name, info=info, stats=stats)


class Stats_Analyzer:
    """Analyze a given stack (array) of system stats (e.g., CPU, MEM) and checks whether the values represent an unusual behavior or not
    """

    @classmethod
    def Analyze_CPU_Usage_Stack(self, cpu_usage_stack, cpu_threshold):
        """Interpret a stack with CPU usages.
        Raises unusual behavior based on the average value of the stack.
        The average is predefined by the user as a `threshold`
        """
        mean_value = round(
            float(sum(cpu_usage_stack) / len(cpu_usage_stack)), 2)
        if(mean_value >= cpu_threshold):
            # print(f'🔥 unusual behavior: {mean_value}≥{cpu_threshold}')
            return [1, mean_value]
        # print(f'✅ normal behavior: {mean_value}<{cpu_threshold}')
        return [0, mean_value]

    @classmethod
    def Analyze_MEM_Usage_Stack(self, mem_usage_stack, mem_threshold):
        """Interpret a stack with MEM usages.
        Raises unusual behavior based on the average value of the stack.
        The average is predefined by the user as a `threshold`
        """
        mean_value = round(
            float(sum(mem_usage_stack) / len(mem_usage_stack)), 2)
        if(mean_value >= mem_threshold):
            # print(f'🔥 unusual behavior: {mean_value}≥{mem_threshold}')
            return [1, mean_value]
        # print(f'✅ normal behavior: {mean_value}<{mem_threshold}')
        return [0, mean_value]


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
                    if(len(machine_id) == 0):
                        machine_id.append(Reader.get_machine_id(last_line))
                except Exception as error:
                    print(f'could not get machine ID')
                    print(f'Reason -> {error}')
                else:
                    pass


class Reader():
    """
    Read content from a log file.
    The reading is done line-by-line.
    Lambdas are built in order to extract different parameters from each event

    Example: `get_cpu_usage` lambda will parse an event line and search for the CPU usage
    """
    get_cpu_usage = lambda log_line: float(log_line[log_line.find(
        'CPU:') + len('CPU:'):log_line.find('%', log_line.find(
            'CPU:'))])

    get_mem_usage = lambda log_line: float(log_line[log_line.find(
        'MEM:') + len('MEM:'):log_line.find('%', log_line.find(
            'MEM:'))])

    get_machine_id = lambda log_line: str(
        log_line[log_line.find('MACHINE-ID:') + len('MACHINE-ID:'):])

    @classmethod
    def Watch_Log_File(self, log_file, execution_time, cycle_time, threshold):
        """Watches a log file for new events.

        With each new event inside the log-file, the data is parsed, and CPU + MEM stats are extracted, each into its own data stack

        `cycle_time` represents the a time window after which the watcher class will analyze the incoming logs. After the analysis of the ingested stats is made, cycle does a reset, clears the event stack and watches for incoming logs again, in order to make a new analysis.

        The watcher function knows when to consider the event stack for a particular field as "Unusual" depending on the value of its corresponding `threshold`.
        The `threshold` argument is an array of values, one for each stat.

        The entire process stops after `execution_time` has been reached.
        """
        event_handler = Modified_State_Handler()

        observer = Observer()
        observer.schedule(event_handler, path=log_file, recursive=False)
        observer.start()

        count = 0
        cycle_count = 0
        watch_state = True

        # set the thresholds for each stat value from the log file
        cpu_threshold = threshold[0]
        mem_threshold = threshold[1]

        total_execution_time = time.time()
        cycle_execution_time = time.time()
        while(watch_state):
            # count the stacks before updating it
            cpu_stack_length_0 = len(cpu_stack)
            mem_stack_length_0 = len(mem_stack)

            # stop if the total execution time has passed
            if(time.time() - total_execution_time >= execution_time):
                print(f'Finished watching the log file')
                watch_state = False
                return

            time.sleep(1)

            # count the stacks after updating it
            cpu_stack_length_1 = len(cpu_stack)
            mem_stack_length_1 = len(mem_stack)

            # stop if no new entries are coming into the stored values
            if((cpu_stack_length_0 == cpu_stack_length_1) or (mem_stack_length_0 == mem_stack_length_1)):
                count += 1
            else:
                count = 0
            if(count == 5):  # stop if the log stream hangs up
                print('No incoming logs...')
                print('Stopping the watcher')
                # print('CPU stack:')
                # print(cpu_stack)
                # print('Memory stack:')
                # print(mem_stack)
                # print('Machine ID')
                # try:
                #     print(machine_id[0])
                # except IndexError as error:
                #     print(machine_id)
                # else:
                #     pass
                watch_state = False
                return

            # continue running the watcher in "batches" of time_window seconds
            if(time.time() - cycle_execution_time >= cycle_time):
                cycle_count += 1
                print(
                    f'{cycle_time} seconds have passed. Completed cycle {cycle_count}')

                # analyze the current stacks for unusual behavior
                # only analyze the stacks that are full in size
                # a full-size stack means a stack that has the proper number of events inside, based on the cycle-window-size and the refresh rate of the logger
                if(len(cpu_stack) == cycle_time):
                    # print(
                    #     f'Analyzing the CPU stats for the past {cycle_time} seconds')
                    cpu_analysis = Stats_Analyzer.Analyze_CPU_Usage_Stack(
                        cpu_stack, cpu_threshold)
                    if(cpu_analysis[0] == 1):
                        print(
                            f'CPU usage is above the threshold! ---> [{cpu_analysis[1]}%] for the past {cycle_time} seconds\nWill alert the DevOps team!!!')
                    else:
                        print(
                            f'CPU usage is normal ---> [{cpu_analysis[1]}%] for the past {cycle_time} seconds. No alert needed.')
                else:
                    # print('cpu stack is skipped -> incomplete')
                    print('Skipping analysis of this cpu usage stack')
                if(len(mem_stack) == cycle_time):
                    # print(
                    #     f'Analyzing the Memory stats for the past {cycle_time} seconds')
                    mem_analysis = Stats_Analyzer.Analyze_MEM_Usage_Stack(
                        mem_stack, mem_threshold)
                    if(mem_analysis[0] == 1):
                        print(
                            f'Memory usage is above the threshold! ---> [{mem_analysis[1]}%] for the past {cycle_time} seconds\nWill alert the DevOps team!!!')
                    else:
                        print(
                            f'Memory usage is normal ---> [{mem_analysis[1]}%] for the past {cycle_time} seconds. No alert needed.')
                else:
                    # print('memory stack is skipped -> incomplete')
                    print('Skipping analysis of this memory usage stack')

                # clear the initial stacks after analysis has been performed
                cpu_stack.clear()
                mem_stack.clear()

                # restart cycle
                cycle_execution_time = time.time()
        observer.stop()


# cpu_stack = []
# mem_stack = []
# machine_id = []
# Reader.Watch_Log_File(log_file_path, 100, 20, [70, 70])

print(Message.Create_Message('RO', 'XX', 'YY'))
