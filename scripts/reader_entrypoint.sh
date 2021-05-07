#!/bin/bash
echo 'Testing the reader implementation'
cd exec/reader/
touch /var/log/dfcti_system_logs.log
chmod +x /var/log/dfcti_system_logs.log
echo 'Setting up the virtual evironment on the machine'
pyenv virtualenv systems
pyenv local systems
python -m pip install --upgrade pip
echo 'Installing pipenv'
pip install pipenv
echo 'Installing the required packages from Pipfile via pipenv'
pipenv install
echo 'Running the unit tests for the reader pipeline'
pipenv run python test_reader.py
echo 'Running the reading pipeline'
pipenv run python dfcti_log_reader.py 