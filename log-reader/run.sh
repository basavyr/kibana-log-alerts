#!/bin/bash
cd ../log-writer/
nohup pipenv run python dfcti_log_writer.py 999 &
cd ../log-reader/
./dfcti_log_reader.py
