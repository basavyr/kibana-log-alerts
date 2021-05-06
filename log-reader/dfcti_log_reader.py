#!/usr/bin/env python3

# import system's related modules
import os
import platform
import time
import sys  # using it for getting command line arguments
from datetime import datetime


# import file watcher module
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import watchdog.events as eventer


# import modules for sending e-mails
import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# import plotting modules
import matplotlib.pyplot as plt
from matplotlib import rc


# use the newly implemented default_rng
import numpy as np
from numpy.random import default_rng
rd = default_rng()


def Get_OS():
    os_value = platform.system()
    return f'{os_value}'


def Create_LogFile_Path():
    """
    Generates a proper file path depending on the running operating system
    Darwin appends a private folder before the entire initial path
    """
    system_os = Get_OS()
    log_file_path = ''
    if(system_os == 'Darwin'):
        log_file_path = '/private/var/log/dfcti_system_logs.log'
    elif(system_os == 'Linux'):
        log_file_path = '/var/log/dfcti_system_logs.log'
    if(log_file_path != ''):
        return log_file_path
    return -1


# Set the path to the log file used for analysis
LOG_FILE_PATH = Create_LogFile_Path()
print(Get_OS())

# define the stacks where each system stat will be stored
# e.g. CPU stack, MEM stack, and Machine ID
cpu_stack = []
mem_stack = []
machine_id = []


def Split_Stack(stack, length):
    """
    **Split a stack:**
    This method takes as input an array and a fixed length and it splits the array into two sub-arrays
    First sub-array has a size of length
    Second sub-array contains the rest of the elements (extra bits)

    Example: [1,2,3,4,5] as initial array
    `length`=3
    -> `[1,2,3]` is the first sub-array and `[4,5]` is the second sub-array
    """
    try:
        sub_array_1 = stack[len(stack) - length:]
        sub_array_2 = stack[0:len(stack) - length]
    except Exception as exc:
        return -1
    else:
        return [sub_array_1, sub_array_2]


# The name and e-mail for each client that needs to be alerted
EMAIL_LIST = [['Test Receive', 'alerts.dfcti.recv@gmail.com']]
# EMAIL_LIST = [['ROBERT-MSFT', 'robert.poenaru@outlook.com'],
#               ['ROBERT-GOOGL', 'robert.poenaru@drd.unibuc.ro']]

# the list of potential issues which can occur during monitoring
RESOURCE_ISSUES = {
    "CPU": "🔥 HIGH CPU USAGE 🔥",
    "MEM": "🔥 HIGH (RAM) MEMORY USAGE 🔥"
}


def Get_Machine_ID(machine_id_file):
    """searches for a machine_id file
    If the file is not present, stops execution!
    """
    ID = ' '
    try:
        with open(machine_id_file, 'r') as id_reader:
            ID = id_reader.read()
    except Exception as error:
        print('Cannot get the Machine-ID\nStopping execution')
    else:
        pass
    if(ID == ' '):
        return -1
    return ID


class Alerter:

    @classmethod
    def Generate_Fail_Stats(self, name, issue, fail_stack):
        stats = [name, issue, fail_stack]
        return stats

    @classmethod
    def Create_Alert(self, stats):
        """Get:
        the name
        +the type of issue which occurred during log monitoring
        +the fail stack

        `stats` -> {name, issue, fail stack}
        """
        name = stats[0]
        issue_info = stats[1]
        issue_stats = stats[2]
        alert_message = Message.Create_Message(name, issue_info, issue_stats)
        return alert_message

    @classmethod
    def SendAlert(self, alert, attachment_files, email):
        """ the files represent the actual stack in a .dat file + the plot file made with matplotlib via CreatePlot class method
        """
        Alerter.Send_Email(email, alert, attachment_files, True)

    @classmethod
    def Send_Email(self, email_address, alert_content, attachment_files, alert_state=False):
        PORT = 465  # For SSL
        ROOT_EMAIL = 'alerts.dfcti@gmail.com'
        UNICORN_ID = 'v2a&tw@uGVWt7%LVjXFD'

        message = MIMEMultipart()
        message["From"] = ROOT_EMAIL
        # https://stackoverflow.com/questions/38151440/can-anyone-tell-my-why-im-getting-the-error-attributeerror-list-object-has
        message["To"] = email_address
        message["Subject"] = f'{str(datetime.utcnow())[:19]} - Alert via DFCTI monitoring system'

        # generating the e-mail body
        message_body = alert_content

        # Adding the body to the actual email
        message.attach(MIMEText(message_body, "plain"))

        # Open the dat file in binary mode
        with open(attachment_files[0], "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part1 = MIMEBase("application", "octet-stream")
            part1.set_payload(attachment.read())

        # Open the plot file in binary mode
        with open(attachment_files[1], "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part2 = MIMEBase("application", "octet-stream")
            part2.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part1)
        encoders.encode_base64(part2)

        # Add header as key/value pair to attachment part
        part1.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_files[0]}",
        )

        # Add header as key/value pair to attachment part
        part2.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_files[1]}",
        )

        # Add attachment to message and convert message to string
        message.attach(part1)
        message.attach(part2)

        final_alert = message.as_string()

        IN_SEND = True
        CONTEXT = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=CONTEXT) as MAIL_SERVER:
            try:
                MAIL_SERVER.login(ROOT_EMAIL, UNICORN_ID)
            except Exception as exc:
                print(f'❌ Cannot log-in!')
                print(f'Reason: {exc}')
            else:
                print(f'🔐 Successful log-in into -> {ROOT_EMAIL}')
                print(f'📤 Ready to send alerts to -> {email_address}')
            if(IN_SEND):
                try:
                    MAIL_SERVER.sendmail(
                        ROOT_EMAIL, email_address, final_alert)
                except Exception as exc:
                    print(f'❌ Cannot send alert to {email_address}...')
                    print(f'Reason: {exc}')
                else:
                    print(f'🚀 Sent alert to {email_address} ! ✅')
            else:
                print('Internal alert system is paused...')
                print('Cannot send alerts at this time ------> #IN_SEND_VALUE:NULL')


class Attachment:
    @classmethod
    def Create_Attachment(self, data, file_path):
        """the incoming file_path contains the .dat file with the fail stack
        second path is the plot
        here, only the first file is required
        """
        with open(file_path[0], 'w+') as attach:
            try:
                # attach.write(str(data) + '\n')
                # use str format for a better compatibility with different data formats
                attach.write(str(data) + '\n')
            except Exception as error:
                print(
                    f'Could not write data at -> {file_path[0]}\nReason: {error}')
                return -1
            else:
                return 1


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

    @classmethod
    def Plot_Stack(self, time_stamp, machine_id, failed_stack, time, threshold, plot_stack_file, labels):
        averages = [np.mean(failed_stack) for _ in range(len(failed_stack))]
        thresholds = [float(threshold) for _ in range(len(failed_stack))]
        if(averages[0] >= thresholds[0]):
            avg_color = '--r'
        else:
            avg_color = '--g'
        # plt.rcParams.update({'font.size': 10})
        # plt.rcParams['figure.dpi'] = 300

        # rc('text', usetex=True)

        plt.figure(figsize=(5, 3.5))
        ax = plt.gca()
        # ax.axes.xaxis.set_visible(False)
        ax.axes.xaxis.set_ticks([])

        plt.plot(failed_stack, '-ok', label=f'{labels}')
        plt.plot(averages, avg_color, label=f'Average Usage')
        plt.plot(thresholds, '-b', label=f'Threshold')
        plt.ylabel(f'%')
        plt.xlabel(f'Last {time} seconds')
        plt.legend(loc='best')
        plt.title(
            f'DFCTI Resource monitor\n@{time_stamp}\nMachine-ID:{machine_id}')
        plt.savefig(plot_stack_file, bbox_inches='tight')
        plt.close()


class Modified_State_Handler(FileSystemEventHandler):
    def on_modified(self, event):
        event_path = event.src_path
        print(event_path)
        if(os.path.isfile(event_path)):
            if(event_path == LOG_FILE_PATH):
                print(f'OS: {Get_OS()}\nLog-File-Path: {event_path}')
                print(f'New log-event in -> {event_path}')

                # easy two-liner for getting the last line of the log-file
                with open(LOG_FILE_PATH, 'r') as reader:
                    last_line = list(reader)[-1]
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
    def Watch_Log_File(cls, log_file_path, execution_time, cycle_time, threshold):
        """Watches a log file for new events.

        With each new event inside the log-file, the data is parsed, and CPU + MEM stats are extracted, each into its own data stack

        `cycle_time` represents the a time window after which the watcher class will analyze the incoming logs. After the analysis of the ingested stats is made, cycle does a reset, clears the event stack and watches for incoming logs again, in order to make a new analysis.

        The watcher function knows when to consider the event stack for a particular field as "Unusual" depending on the value of its corresponding `threshold`.
        The `threshold` argument is an array of values, one for each stat. Order: `CPU` and `MEM`

        The entire process stops after `execution_time` has been reached.
        """
        event_handler = Modified_State_Handler()

        observer = Observer()
        observer.schedule(event_handler, path=log_file_path, recursive=False)

        count = 0
        watch_state = True

        # set the thresholds for each stat value from the log file
        try:
            cpu_threshold = threshold[0]
            mem_threshold = threshold[1]
        except Exception as error:
            print(f'The threshold values are incompatible with the current log format.')
        else:
            pass

        observer.start()
        total_execution_time = time.time()
        cycle_time_start = time.time()
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

            # count the stacks after updating them
            # stack update takes place after 1 second passes
            cpu_stack_length_1 = len(cpu_stack)
            mem_stack_length_1 = len(mem_stack)

            # stop if no new entries are coming into the stacks
            # hangs up the ingest after 5 seconds
            if((cpu_stack_length_0 == cpu_stack_length_1) or (mem_stack_length_0 == mem_stack_length_1)):
                count += 1
            else:
                count = 0

            # stop after 10 seconds
            if(count == 10):  # stop if the logging pipeline hangs up
                print('No incoming logs...')
                print('Stopping the watcher')
                watch_state = False
                return

            # analyze the current stacks for unusual behavior
            # only analyze the stacks that are full in size
            # a full-size stack means it has a proper number of events inside, based on the cycle-window-size and the refresh rate of the logger itself
            # use the split-stack method in order to make sure that the stacks have exactly the required size (given by cycle_time)
            if(time.time() - cycle_time_start >= cycle_time):
                print(f'{cycle_time} seconds passed. Analyzing the stacks')

                # analyze the CPU resource
                if(len(cpu_stack) >= cycle_time):
                    # make sure the cpu stack only contains exactly `cycle_time` elements
                    # only use latest added elements in the stack
                    adjusted_cpu_stack = Split_Stack(cpu_stack, cycle_time)[0]
                    cpu_analysis = Stats_Analyzer.Analyze_CPU_Usage_Stack(
                        adjusted_cpu_stack, cpu_threshold)
                    if(cpu_analysis[0] == 1):
                        print(
                            f'CPU usage is above the threshold! ---> [{cpu_analysis[1]}%] for the past {cycle_time} seconds\nWill alert the DevOps team!!!')
                        cpu_fail_value = f'AVG_CPU_USAGE for the past {cycle_time} seconds: {cpu_analysis[1]}%, which is above the threshold value {cpu_threshold}%.'
                        for email in EMAIL_LIST:
                            fail_stats = Alerter.Generate_Fail_Stats(
                                email[0], RESOURCE_ISSUES["CPU"], cpu_fail_value)
                            alert = Alerter.Create_Alert(fail_stats)

                            # generate plot with cpu usage during the cycle time
                            # this is a graphical representation with the behavior of the resource during the cycle time
                            Stats_Analyzer.Plot_Stack(datetime.utcnow(
                            ), machine_id[0], adjusted_cpu_stack, cycle_time, cpu_threshold, 'cpu_usage.pdf', 'CPU Usage')

                            # create attachment for the e-mail alert
                            # contains the stack `.dat` file and the graphical representation of the usage
                            attach_filenames = [
                                'fail_stack.dat', 'cpu_usage.pdf']

                            # create the fail stack `.dat` file
                            Attachment.Create_Attachment(
                                f'{datetime.utcnow()} ----->  CPU_FAIL_STACK: {adjusted_cpu_stack}\n{cpu_fail_value}', attach_filenames)

                            # send email with attachment
                            Alerter.SendAlert(
                                alert, attach_filenames, email[1])
                    else:
                        print(
                            f'CPU usage is normal ---> [{cpu_analysis[1]}%] for the past {cycle_time} seconds. No alert needed.')
                        pass
                    # clear the stacks after analysis has been performed
                    cpu_stack.clear()

                # analyze the memory resource
                if(len(mem_stack) >= cycle_time):
                    # make sure the memory stack only contains exactly `cycle_time` elements
                    # only use latest added elements in the stack
                    adjusted_mem_stack = Split_Stack(mem_stack, cycle_time)[0]
                    mem_analysis = Stats_Analyzer.Analyze_MEM_Usage_Stack(
                        adjusted_mem_stack, mem_threshold)
                    if(mem_analysis[0] == 1):
                        print(
                            f'Memory usage is above the threshold! ---> [{mem_analysis[1]}%] for the past {cycle_time} seconds\nWill alert the DevOps team!!!')
                        mem_fail_value = f'AVG_MEM_USAGE for the past {cycle_time} seconds: {mem_analysis[1]}%, which is above the threshold value {mem_threshold}%.'
                        for email in EMAIL_LIST:
                            fail_stats = Alerter.Generate_Fail_Stats(
                                email[0], RESOURCE_ISSUES["MEM"], mem_fail_value)
                            alert = Alerter.Create_Alert(fail_stats)

                            # generate plot with memory usage during the cycle time
                            # this is a graphical representation with the behavior of the resource during the cycle time
                            Stats_Analyzer.Plot_Stack(datetime.utcnow(
                            ), machine_id[0], adjusted_mem_stack, cycle_time, mem_threshold, 'mem_usage.pdf', 'MEM Usage')

                            # create attachment for the e-mail alert
                            # contains the stack `.dat` file and the graphical representation of the usage
                            attach_filenames = [
                                'fail_stack.dat', 'mem_usage.pdf']

                            # create the fail stack `.dat` file
                            Attachment.Create_Attachment(
                                f'{datetime.utcnow()} ----->  MEM_FAIL_STACK: {adjusted_mem_stack}\n{mem_fail_value}', attach_filenames)

                            # send email with attachment
                            Alerter.SendAlert(
                                alert, attach_filenames, email[1])
                    else:
                        print(
                            f'Memory usage is normal ---> [{mem_analysis[1]}%] for the past {cycle_time} seconds. No alert needed.')
                        pass
                    # clear the stacks after analysis has been performed
                    mem_stack.clear()

                cycle_time_start = time.time()

        # observer.stop()
        # observer.join()


def Do_Asymmetric_Test():
    # giving default (safe-mode) values for the total execution time in case no cli args are set by the user
    timer = 69
    cycle_time = 5
    try:
        timer = int(sys.argv[1])
    except IndexError as err:
        print('No argument given!\nDefaulting to the safe values')
    else:
        try:
            cycle_time = int(sys.argv[2])
        except IndexError as err:
            print('No cycle time given!\nDefaulting to the safe value')
        else:
            pass
    print(LOG_FILE_PATH)

    # only continue if the arguments are properly given from the CLI
    execute = False
    if(timer < cycle_time):
        print('Cannot start the execution pipeline')
        return
    else:
        execute = True

    # test the asymmetric stack update
    if(execute):
        print(f'You have selected following settings:')
        print(f'Total execution time of the script: {timer} s')
        print(
            f'Each log analysis will be performed after a window of {cycle_time} s')
        cycle_count = 0

        event_handler = Modified_State_Handler()
        observer = Observer()
        observer.schedule(event_handler, path=LOG_FILE_PATH, recursive=False)

        observer.start()
        cycle_time_start = time.time()
        while(timer):

            cycle_count += 1

            print(cpu_stack, mem_stack)
            # time passes
            time.sleep(1)

            print(cpu_stack, mem_stack)
            if(time.time() - cycle_time_start >= cycle_time):
                print(f'{cycle_time} seconds passed. Analyzing the stacks')
                if(len(cpu_stack) >= cycle_time):
                    print(f'Full stack:{cpu_stack}')
                    cpu_stack_full = Split_Stack(cpu_stack, cycle_time)
                    print(f'Will do operations with:')
                    print(f'cpu_stack-> {cpu_stack_full[0]}')
                    l1 = len(cpu_stack_full[0])
                    print(f'throws-> {cpu_stack_full[1]}')
                    extra_time = rd.choice([1, 2, 3, 4, 5])
                    time.sleep(extra_time)
                    print(f'Pausing thread for {extra_time}')
                    cpu_stack.clear()

                if(len(mem_stack) >= cycle_time):
                    print(f'Full stack:{mem_stack}')
                    mem_stack_full = Split_Stack(mem_stack, cycle_time)
                    l2 = len(mem_stack_full[0])
                    print(f'mem_stack-> {mem_stack_full[0]}')
                    print(f'throws-> {mem_stack_full[1]}')
                    extra_time = rd.choice([4, 5, 6, 7, 8])
                    time.sleep(extra_time)
                    print(f'Pausing thread for {extra_time}')
                    mem_stack.clear()

                # if(l1 == l2):
                #     print('cycle PASSED the stack-append test')
                # else:
                #     print('cycle FAILED the stack-append test')
                cycle_time_start = time.time()

            else:
                pass

            timer -= 1
        observer.stop()
        observer.join()
        print(f'Finished {int(cycle_count/cycle_time)} watch cycles')
    else:
        pass


def Read_Pipeline():
    Reader.Watch_Log_File(LOG_FILE_PATH, 20,
                          5, [70, 70])


if __name__ == "__main__":
    with open('/private/var/log/dfcti_system_logs.log', 'r+') as logger:
        text = logger.readlines()
        print(len(text))
    Do_Asymmetric_Test()
    # Read_Pipeline()
