#!/bin/bash
cd ../log-writer/
nohup pipenv run python dfcti_log_writer.py 250 &
cd ../log-reader/
pipenv run python dfcti_log_reader.py
