import os
import helpers


pid_file = os.path.join('tmp', 'pymapmaker.pid')


def check_running():
    is_running = os.path.exists(pid_file)
    return is_running


def start_process():
    pid = str(os.getpid())
    if not check_running():
        # os.system(run script here)
        helpers.write_to_log("Program Started at " + helpers.start_time)
        helpers.write_to_log("Starting process with pid: " + pid)
        f = open(pid_file, 'w')
        f.write(pid)
        f.close()
    else:
        helpers.write_to_log("Tried to start process but process is already running with pid: " + pid)


def end_process():
    end_time = helpers.get_time()
    delta = int(end_time) - int(helpers.start_time)
    helpers.write_to_log("Process took " + str(delta) + " seconds to finish.")
    helpers.set_run_time()
    os.remove(pid_file)



