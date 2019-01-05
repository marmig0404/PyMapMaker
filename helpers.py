# helpers.py includes helper methods for pymapmaker
import csv
import datetime
import os
import sys
import time

from backports import configparser

import database
from errors import MissingLastRunTime, MissingPastMapsList

start_time = str(round(time.time(), 0))
config_file = "config.ini"
private_config_file = "privateConfig.ini"
temp_dir = 'tmp'
address2img_config_file = os.path.join('address2img', 'config.ini')
last_run_file_location = os.path.join(temp_dir, 'last.time')
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


def write_to_log(data_to_write):
    # writes function input to log file and terminal output
    print(data_to_write)
    log_file_location = os.path.join(log_directory, "log-" + log_time_string + ".txt")
    log_file = open(log_file_location, "a+")
    log_file.write("(" + log_time_string + "/" + start_time + ") " + data_to_write + "\n")
    log_file.close()


def read_private_config(section, key):
    # reads PRIVATE_CONFIG_FILE, returns value of section and key
    parser = configparser.ConfigParser()
    parser.read(private_config_file)
    value = parser.get(section, key)
    return value


def get_config(section, key):
    # reads CONFIG_FILE, returns value of specified section and key
    parser = configparser.ConfigParser()
    parser.read(config_file)
    in_development = (parser.get("General Config", "Version Status") == "development")
    in_production = (parser.get("General Config", "Version Status") == "production")
    if (not in_development) and (not in_production):
        write_to_log("Error: Invalid Version Status")
        sys.exit(2)
    if (not in_development) and (section == "Address Database Config" or section == "Map Database Config"):
        value = read_private_config(section, key)
    else:
        value = parser.get(section, key)
    return value


def get_all_config(section, keys):
    values = dict()
    for key in keys:
        value = {key: get_config(section, key)}
        values.update(value)
    return values


def get_database_config(database_type):
    # reads config file specifically for database configuration and then returns database
    if database_type == "address":
        host = get_config("Address Database Config", "Host")
        port = get_config("Address Database Config", "Port")
        dbname = get_config("Address Database Config", "Database Name")
        username = get_config("Address Database Config", "Username")
        password = get_config("Address Database Config", "Password")
        table = get_config("Address Database Config", "Table")
        address_column = get_config("Address Database Config", "Address Column Name")
        last_modified_column = get_config("Address Database Config", "Last Modified Column Name")
        return_database = database.MySQL(host, port, dbname, username, password, table, address_column,
                                         last_modified_column)
    # elif database_type == "map":
    #     host = get_config("Map Database Config", "Host")
    #     port = get_config("Map Database Config", "Port")
    #     dbname = get_config("Map Database Config", "Database Name")
    #     username = get_config("Map Database Config", "Username")
    #     password = get_config("Map Database Config", "Password")
    #     schema = get_config("Map Database Config", "Database Schema")
    #     table_names = get_config("Map Database Config", "Table Names")
    #     geometry_columns = get_config("Map Database Config", "Geometry Columns")
    #     return_database = database.PGSQL(host, port, dbname, username, password, schema, table_names, geometry_columns

    else:
        return_database = None

    return return_database


def get_last_run_time():
    # reads file named last.time from ./logs to see the last time the program was ran
    try:
        last_run_file = open(os.path.join('logs', 'last.time'), "r")
        last_run_time_data = last_run_file.read()
        last_run_file.close()
        if os.path.exists(last_run_file_location):
            os.remove(last_run_file_location)
        return last_run_time_data
    except IOError:
        return 0


def get_time():
    return str(round(time.time(), 0))


def save_maps(maps):
    maps_file_location = os.path.join(log_directory, "maps-" + log_time_string + ".csv")
    with open(maps_file_location, mode='w') as map_file:
        map_writer = csv.writer(map_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for address, name in maps:
            map_writer.writerow([address, name])


def get_new_addresses(addresses):
    last_time_location = os.path.join(temp_dir, 'last.time')
    if os.path.isfile(last_time_location):

        formatted_last_time = time.strftime(time.localtime(int(last_run_time)))
        maps_file_location = os.path.join(log_directory, "maps-" + formatted_last_time + ".csv")
        if os.path.isfile(maps_file_location):

            old_addresses = []
            with open(maps_file_location, mode='r') as map_file:

                csv_reader = csv.DictReader(map_file)
                for row in csv_reader:
                    old_addresses.append(row[0])
            return set(addresses).intersection(set(old_addresses))

        else:
            raise MissingPastMapsList('Cannot locate csv file indicating previous maps')
    else:
        raise MissingLastRunTime('Cannot locate temp file saving last run time')


last_run_time = get_last_run_time()
naming_scheme = get_config("General Config", "Log Naming Scheme")
log_time = datetime.datetime.now()
log_time_string = log_time.strftime(naming_scheme)
