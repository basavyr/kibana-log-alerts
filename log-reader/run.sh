#!/bin/bash
cd ../log-writer/
nohup ./dfcti_log_writer.py 999 &
cd ../log-reader/
./dfcti_log_reader.py
