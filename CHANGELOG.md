## Alert System @`cloudifin`

### Latest updates 

* Multiple improvements for the documentation of the classes and their corresponding attributes, methods and so on.
* Clean and consistent output in case any errors might occur during the reading pipeline.
* Optimized the conditions for sending alerts with regards to the monitored system logs
* Improved the way of sending alerts to the client list
* Docker container for testing the methods in `log-reader` and `log-writer` was configured
* Debug mode for the reader has been improved, and it is more consistent with the `watchdog` *event handler*
* Improved the writer log by adding `__name__`, such that certain methods are not executed within the unit tests
* Improved the reader log by adding `__name__`, such that certain methods are not executed within the unit tests
* Improved pipeline for docker
* Add unit tests for writing logs
* Add unit tests for reading logs
* Properly configured the `grok` filter to organize the event fields in a consistent way
* Add graph visualizations for the CPU usage inside Kibana.
* Add pipeline for Logstash
* Uses `grok` filter for the extraction of system stats from the event logs
* Add command line arguments for the python **reading** and **writing** implementations
* Improved error handling
* Properly updates the stacks for each stat in particular based on the pre-configured `cycle_count`
* The analysis of the stats is made continuously, with clearing the data stacks after each cycle period.
* Get the last log event in a simpler way
* Get the OS version of the running resource
* Adapts the path of the output log-file for different platforms
* Modified the reader script to use a proper machine-ID
* Thresholds are converted into float throughout the codebase
* Uses only one e-mail address for computational speed
* Add class functions for creating a machine-ID on any compute resource that is running the writer script
* Add class function for getting the machine-ID from the specific file within the reader script
* Add commands in the GitHub Actions for running the log writer in the background
* Changed the structure of the `resource` folder
* Added class for attachment
* Add alert class-module with support for mail alerts -> `dfcti_log_reader.py`
* Add archive with the log writer script
* Improves the pipeline for uploading artifact to the current release tag
* Added correct versioning
* Removed action trigger when pushing on main without tag
