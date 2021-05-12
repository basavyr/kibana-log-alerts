#!/usr/bin/env bash
cd ../log-writer/
nohup pipenv run python dfcti_log_writer.py 100 &
cd ../log-reader/
pipenv run python dfcti_log_reader.py 20