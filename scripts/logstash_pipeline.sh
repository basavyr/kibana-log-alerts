#!/usr/bin/env bash
cycle_time=$2

node_name=$(uname -n)
elk_node_name='elk.nipne.ro'

logstash_executable=/usr/share/logstash/bin/logstash 

virtualenvName=systems

log_file_path=/var/log/dfcti_system_logs.log

if [ $node_name == $elk_node_name ];
then
    echo 'Creating the log file....'
    touch $log_file_path
    chmod 777 $log_file_path
    cd ../log-reader/
    echo 'Reader -> Activating a virtual environment and installing packages from the Pipfile...'
    pyenv virtualenv $virtualenvName
    pyenv local $virtualenvName
    python -m pip install --upgrade pip
    python -m pip install pipenv
    pipenv install
    echo 'Writer -> Activating a virtual environment and installing packages from the Pipfile...'
    cd ../log-writer/
    pyenv local $virtualenvName
    pipenv install
    nohup pipenv run python dfcti_log_writer.py $1 &
    cd ../log-reader/
    nohup pipenv run python dfcti_log_reader.py $2 &
    cd ../resources/pipelines/
    sudo nohup $logstash_executable -f py_logs.conf --config.reload.automatic &
else
    echo Cannot run the script on this node.
fi