import os
import time

import helpers
from errors import InstanceError

temp_dir = helpers.temp_dir
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
pid_file = os.path.join(temp_dir, 'pymapmaker.pid')



def check_running():
    is_running = os.path.exists(pid_file)
    return is_running


def start_process():
    pid = str(os.getpid())
    if not check_running():
        start_time = time.localtime(float(helpers.start_time))
        start_time_string = time.strftime('%Y-%m-%d %H:%M:%S', start_time)
        helpers.write_to_log("Starting process with pid: " + pid)
        helpers.write_to_log("Process started at " + start_time_string)
        f = open(pid_file, 'w')
        f.write(pid)
        f.close()

    else:
        helpers.write_to_log("Tried to start process but process is already running with pid: " + pid)
        raise InstanceError('Instance already running with pid: ' + pid)


def set_run_time():
    # updates the last.time file for next run
    last_run_file = open(helpers.last_run_file_location, "w")
    last_run_file.write(str(helpers.log_time))
    last_run_file.close()


def end_process():
    if check_running():
        start_time_epoch = float(helpers.start_time)
        end_time_epoch = float(helpers.get_time())
        end_time = time.localtime(end_time_epoch)
        end_time_string = time.strftime('%Y-%m-%d %H:%M:%S', end_time)
        delta = end_time_epoch - start_time_epoch
        helpers.write_to_log("Ending process at " + end_time_string)
        helpers.write_to_log("Process took " + str(delta) + " seconds to finish.")
        set_run_time()
        os.remove(pid_file)
    else:
        helpers.write_to_log("Tried to end process but it appears the process was never started.")
