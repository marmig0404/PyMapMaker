class Error(Exception):
    pass


class InstanceError(Error):
    # Error is thrown when PID file is detected and has a value
    # This indicates either a cleanup failure from last program run
    # or that another instance of the program is already running
    def __init__(self, message):
        self.message = message


class MissingLastRunTime(Error):
    # Error is thrown when last.time is not found in the temporary directory
    # This error is not fatal, but prevents the program from being ran in append mode
    # forcing overwrite mode
    def __init__(self, message):
        self.message = message


class MissingPastMapsList(Error):
    # Error is thrown when the csv file containing map addresses and names
    # with the timestamp of the last run is not found. Similar to MissingLastRunTime,
    # the process is not fatal, but forces overwrite mode.
    def __init__(self, message):
        self.message = message
