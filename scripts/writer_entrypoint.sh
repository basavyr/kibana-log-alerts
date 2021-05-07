#!/bin/bash
touch /var/log/dfcti_system_logs.log
chmod +x /var/log/dfcti_system_logs.log
echo 'Testing the writer implementation'
cd exec/writer/
pyenv virtualenv systems
pyenv local systems
python -m pip install --upgrade pip
pip install pipenv
pipenv install
echo 'Run the Unit Tests'
pipenv run python test_writer.py
echo 'Run the Log-Writer pipeline'
pipenv run python dfcti_log_writer.py 10
cat /var/log/dfcti_system_logs.log