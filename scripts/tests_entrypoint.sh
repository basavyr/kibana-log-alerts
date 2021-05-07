#!/bin/bash
touch /var/log/dfcti_system_logs.log
chmod +x /var/log/dfcti_system_logs.log
echo 'Testing the reader implementation'
cd exec/reader/
pyenv virtualenv systems
pyenv local systems
python -m pip install --upgrade pip
pip install pipenv
pipenv install
# pipenv run python dfcti_log_reader.py 11 5
pipenv run python test_reader.py
cd ../writer/
pyenv local systems
pipenv install
#pipenv run python dfcti_log_writer.py 10
pipenv run python test_writer.py
cat /var/log/dfcti_system_logs.log