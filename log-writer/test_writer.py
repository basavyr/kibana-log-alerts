#!/usr/bin/env python3
import dfcti_log_writer as logwriter
import unittest
import time


class Test(unittest.TestCase):
    writer = logwriter.Write_Logs(logwriter.log_file_path)
    system = logwriter.SystemLogs()
    log_file_path = logwriter.log_file_path
    logs = []
    REFRESH_CYCLE = logwriter.REFRESH_CYCLE
    machine_id = logwriter.MachineID.Get_Machine_ID()
    machine_id_length = len(machine_id)

    def test_Machine_ID(self):
        print(f'Starting the test for MACHINE_ID generation\n')

        self.assertNotEqual(self.machine_id_length, 0)
        self.assertNotEqual(self.machine_id, '')
        self.assertNotEqual(self.machine_id, ' ')
        print(f'Finished the test for MACHINE_ID generation\n')

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
            time.sleep(self.REFRESH_CYCLE)
        end_time = time.time()
        self.assertEqual(len(self.logs), n_iterations)
        self.assertGreaterEqual(end_time - start_time,
                                self.REFRESH_CYCLE * n_iterations)
        print(f'Finished the test for generating system stats')

    def test_Write_Log_Line(self):
        print(f'Starting the test for writing logs')
        n_iterations = 10
        log_lines = []

        for idx in range(n_iterations):
            line = self.writer.Generate_System_Log_Line(self.machine_id)
            self.assertIsNotNone(line)
            log_lines.append(line)
            self.assertGreaterEqual(len(log_lines), 0)

        for line in log_lines:
            yy_liner = self.writer.Write_Log_Line(line, self.log_file_path)
            self.assertEqual(yy_liner, 1)
        print(f'Finished the test for writing logs')

    def test_Write_Process(self):
        print(f'Started the test for the Write Process')
        n_tests = 5
        for idx in range(n_tests):
            print(f'SUBTEST -----> {idx+1}/{n_tests}')
            wp = self.writer.Write_Process(
                10, self.REFRESH_CYCLE, self.log_file_path, self.machine_id)
            self.assertIsNot(wp, -1)

        print(f'Finished  the test for the Write Process')


if __name__ == '__main__':
    unittest.main()
