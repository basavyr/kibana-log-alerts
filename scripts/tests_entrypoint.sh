#!/bin/bash
touch /var/log/dfcti_system_logs.log
chmod 777 /var/log/dfcti_system_logs.log
echo 'Testing the reader implementation'
cd exec/reader/
pyenv virtualenv systems
pyenv local systems
python -m pip install --upgrade pip
pip install pipenv
pipenv install
# pipenv run python dfcti_log_reader.py 11 5
echo 'Run the reader test'
pipenv run python test_reader.py
cd ../writer/
pyenv local systems
pipenv install
#pipenv run python dfcti_log_writer.py 10
echo 'Run the writer test'
pipenv run python test_writer.py
cat /var/log/dfcti_system_logs.log