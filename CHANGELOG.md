# Alert System 

## Latest updates 

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
