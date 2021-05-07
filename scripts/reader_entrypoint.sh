#!/bin/bash
echo 'Testing the reader implementation'
cd exec/reader/
touch /var/log/dfcti_system_logs.log
chmod +x /var/log/dfcti_system_logs.log
pyenv virtualenv systems
pyenv local systems
python -m pip install --upgrade pip
pip install pipenv
pipenv install
pipenv run python dfcti_log_reader.py 11 5
pipenv run python test_reader.py