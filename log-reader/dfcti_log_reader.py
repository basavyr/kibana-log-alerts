#!/usr/bin/env python3


# import system's related modules
import os
import platform
import time
from datetime import datetime


# import file watcher module
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# import modules for second e-mails
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
    system_os = Get_OS()
    log_file_path = ''
    if(system_os == 'Darwin'):
        log_file_path = 'This is macOS'
    elif(system_os == 'Linux'):
        log_file_path = 'This is Linux'
    return log_file_path


# Set the path to the log file used for analysis
log_file_path = '/var/log/dfcti_system_logs.log'

# The name and e-mail for each client that needs to be alerted
EMAIL_LIST = [['ROBERT-MSFT', 'robert.poenaru@outlook.com']]
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
            attach.write(data + '\n')


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
        print(f'event: {event.src_path}')
        # if(event_path == '/private' + log_file_path):
        # if(event_path == log_file_path):
        # print(f'The modified log_file path is: {event_path}')
        #     with open(log_file_path, 'r') as reader:
        #         content = reader.readlines()
        #         last_line = content[-1]
        #         try:
        #             # must append only the value of the cpu or memory
        #             cpu_stack.append(Reader.get_cpu_usage(last_line))
        #         except Exception as error:
        #             print(f'could not add CPU stats into the cpu stack')
        #             print(f'Reason -> {error}')
        #         else:
        #             pass
        #         try:
        #             # must append only the value of the cpu or memory
        #             mem_stack.append(Reader.get_mem_usage(last_line))
        #         except Exception as error:
        #             print(f'could not add MEM stats into the cpu stack')
        #             print(f'Reason -> {error}')
        #         else:
        #             pass
        #         try:
        #             if(len(machine_id) == 0):
        #                 machine_id.append(Reader.get_machine_id(last_line))
        #         except Exception as error:
        #             print(f'could not get machine ID')
        #             print(f'Reason -> {error}')
        #         else:
        #             pass


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
                        cpu_fail_value = f'AVG_CPU_USAGE for the past {cycle_time} seconds: {cpu_analysis[1]}%, which is above the threshold value {cpu_threshold}%.'
                        for email in EMAIL_LIST:
                            fail_stats = Alerter.Generate_Fail_Stats(
                                email[0], RESOURCE_ISSUES["CPU"], cpu_fail_value)
                            alert = Alerter.Create_Alert(fail_stats)

                            # generate plot with cpu usage during the cycle time
                            Stats_Analyzer.Plot_Stack(datetime.utcnow(
                            ), machine_id[0], cpu_stack, cycle_time, cpu_threshold, 'cpu_usage.pdf', 'CPU Usage')

                            # create attachment for the e-mail alert
                            attach_filenames = [
                                'fail_stack.dat', 'cpu_usage.pdf']
                            Attachment.Create_Attachment(
                                f'{datetime.utcnow()} ----->  CPU_FAIL_STACK: {cpu_stack}\n{cpu_fail_value}', attach_filenames)

                            # send email with attachement
                            Alerter.SendAlert(
                                alert, attach_filenames, email[1])
                    else:
                        print(
                            f'CPU usage is normal ---> [{cpu_analysis[1]}%] for the past {cycle_time} seconds. No alert needed.')
                        pass
                else:
                    print(
                        'Skipping analysis of this CPU usage stack.\nReason: Not enough data to perform analysis')
                if(len(mem_stack) == cycle_time):
                    mem_analysis = Stats_Analyzer.Analyze_MEM_Usage_Stack(
                        mem_stack, mem_threshold)
                    if(mem_analysis[0] == 1):
                        print(
                            f'Memory usage is above the threshold! ---> [{mem_analysis[1]}%] for the past {cycle_time} seconds\nWill alert the DevOps team!!!')
                        mem_fail_value = f'AVG_MEM_USAGE for the past {cycle_time} seconds: {mem_analysis[1]}%, which is above the threshold value {mem_threshold}%.'
                        for email in EMAIL_LIST:
                            fail_stats = Alerter.Generate_Fail_Stats(
                                email[0], RESOURCE_ISSUES["MEM"], mem_fail_value)
                            alert = Alerter.Create_Alert(fail_stats)

                            # generate plot with cpu usage during the cycle time
                            Stats_Analyzer.Plot_Stack(datetime.utcnow(
                            ), machine_id[0], mem_stack, cycle_time, mem_threshold, 'mem_usage.pdf', 'MEM Usage')

                            # create attachment for the e-mail alert
                            attach_filenames = [
                                'fail_stack.dat', 'mem_usage.pdf']

                            Attachment.Create_Attachment(
                                f'{datetime.utcnow()} ----->  MEM_FAIL_STACK: {mem_stack}\n{mem_fail_value}', attach_filenames)

                            # send email with attachment
                            Alerter.SendAlert(
                                alert, attach_filenames, email[1])
                    else:
                        print(
                            f'Memory usage is normal ---> [{mem_analysis[1]}%] for the past {cycle_time} seconds. No alert needed.')
                        pass
                else:
                    print(
                        'Skipping analysis of this memory usage stack.\nReason: Not enough data to perform analysis')

                # clear the initial stacks after analysis has been performed
                cpu_stack.clear()
                mem_stack.clear()

                # restart cycle
                cycle_execution_time = time.time()
        observer.stop()


cpu_stack = []
mem_stack = []
machine_id = []

# Reader.Watch_Log_File(log_file_path, 600, 60, [70, 70])

event_handler = Modified_State_Handler()
observer = Observer()
observer.schedule(event_handler, path=log_file_path, recursive=False)

count = 0
run = True
print(Create_LogFile_Path())
observer.start()
while(run):
    # try:
    # except RuntimeError as err:
    #     observer.stop()
    #     run = False
    # finally:
    count += 1
    time.sleep(1)
    if(count == 3):
        run = False
observer.stop()


