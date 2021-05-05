#!/usr/bin/env python3
import dfcti_log_writer as logwriter
import unittest
import time


class Test(unittest.TestCase):
    writer = logwriter.Write_Logs()
    system = logwriter.SystemLogs()
    logs = []

    def test_Machine_ID(self):
        print(f'Starting the test for MACHINE_ID generation\n')
        machine_id_length = len(logwriter.MACHINE_ID)
        self.assertNotEqual(machine_id_length, 0)
        print(f'Finsihed the test for MACHINE_ID generation\n')

    def test_Generate_System_Log_Line(self):
        print(f'Starting the test for generating system stats')
        n_iterations = 10
        start_time = time.time()
        for idx in range(n_iterations):
            cpu_stat = self.system.Get_CPU_Usage()
            mem_stat = self.system.Get_MEM_Usage()
            self.assertIsNotNone(cpu_stat)
            self.assertIsNotNone(mem_stat)
            line = [cpu_stat, mem_stat]
            self.logs.append(line)
            time.sleep(logwriter.REFRESH_CYCLE)
        end_time = time.time()
        self.assertEqual(len(self.logs), n_iterations)
        self.assertGreaterEqual(end_time - start_time,
                                logwriter.REFRESH_CYCLE * n_iterations)
        print(f'Finished the test for generating system stats')

    def test_Write_Log_Line(self):
        print(f'Starting the test for writing logs')
        n_iterations = 10
        log_file_path = logwriter.log_file_path
        log_lines = []

        for idx in range(n_iterations):
            line = self.writer.Generate_System_Log_Line()
            self.assertIsNotNone(line)
            log_lines.append(line)
            self.assertGreaterEqual(len(log_lines), 0)

        for line in log_lines:
            yy_liner = self.writer.Write_Log_Line(line, log_file_path)
            self.assertEqual(yy_liner, 1)
        print(f'Finished the test for writing logs')


if __name__ == '__main__':
    unittest.main()
