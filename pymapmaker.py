import sched
import sys
import time

import helpers
import running
from address2img import map_maker
from errors import MissingLastRunTime, MissingPastMapsList


def loop(config_file):
    # initialize database
    address_database = helpers.get_database_config('address')

    # retrieve addresses from database
    sql_query = 'get some addreses'
    addresses = address_database.make_query(sql_query)

    # close database connection

    # address filtering
    automatic_mode = (helpers.get_config('Automatic Mode Config', 'Enabled') == 'True')
    append_mode = (helpers.get_config('Automatic Mode Config', 'Operation Type') == 'Append')
    if automatic_mode and append_mode:
        try:
            addresses = helpers.get_new_addresses(addresses)
        except (MissingLastRunTime, MissingPastMapsList):
            helpers.write_to_log("Cannot run in append mode, switching to overwrite.")

    # use address2img, pass addresses and config.ini file
    map_worker = map_maker.Map_Maker(addresses, config_file)
    maps = map_worker.make_maps()

    # update list of maps made
    helpers.save_maps(maps)

try:
    running.start_process()
except running.InstanceError:
    helpers.write_to_log("Too many instances of process are running, exiting...")
    sys.exit()
period_hr = float(helpers.get_config('Automatic Mode Config', 'Interval'))
period_sec = period_hr # * 3600
scheduler = sched.scheduler(time.time, time.sleep)
config_file = helpers.config_file
scheduler.enter(0, 10, loop, config_file)
try:
    while True:
        scheduler.enter(delay=period_sec, priority=1, action=loop, argument=config_file)
        scheduler.run()
except KeyboardInterrupt:
    helpers.write_to_log("Process interrupted.")
    pass

running.end_process()



