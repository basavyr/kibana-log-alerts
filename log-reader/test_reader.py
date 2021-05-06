#!/usr/bin/env python3
import dfcti_log_reader as logreader
import unittest
import time
import numpy as np
from numpy.random import default_rng

rd = default_rng()


class Test(unittest.TestCase):
    n_iterations = 25
    test_data = []
    alerter = logreader.Alerter()
    message = logreader.Message()
    reader = logreader.Reader()

    def test_Create_LogFile_Path(self):
        """Testing the creation of log file paths
        Depends on the actual operating system.
        """
        print('Started the log path creation test\n')
        for _ in range(self.n_iterations):
            yy_path = logreader.Create_LogFile_Path()
            self.assertIsNotNone(yy_path)
            self.assertNotEqual(yy_path, -1)
            self.test_data.append(yy_path)
        self.assertEqual(len(self.test_data), self.n_iterations)
        print('Finished the log path creation test\n')

    def test_Split_Stack(self):
        """Checks how the stack is split in two sub-stacks
        """
        print('started test for splitting the logs\n')
        for _ in range(self.n_iterations):
            initial_stack = rd.integers(1, 10, 20)
            length = rd.integers(1, 9)
            yy_data = logreader.Split_Stack(initial_stack, length)
            self.assertNotEqual(yy_data, -1)
            self.assertEqual(len(yy_data[0]) +
                             len(yy_data[1]), len(initial_stack))
        print('Finished splitting the logs\n')

    def test_Create_Alert(self):
        print('Started testing the alert creation the logs\n')
        fail_stats = 'stats'
        fake_stats = ['Name', 'An issue', fail_stats]
        for _ in range(self.n_iterations):
            yy_data = self.alerter.Create_Alert(fake_stats)
            self.assertIsNotNone(yy_data)
            self.assertNotEqual(len(yy_data), 0)
            self.assertNotEqual(len(yy_data), 1)
            self.assertNotEqual(len(yy_data), 2)
        print('Finished testing the alert creation the logs\n')

    def test_Create_Attachment(self):
        print('testing the creation of attachments\n')
        paths = ['1', '2']
        yy_proc = logreader.Attachment().Create_Attachment(
            ['Some data', 'Some more data'], paths)
        self.assertIsNotNone(yy_proc)
        self.assertNotEqual(yy_proc, -1)
        self.assertEqual(yy_proc, 1)
        print('finished testing the creation of attachments\n')


if __name__ == '__main__':
    unittest.main()
