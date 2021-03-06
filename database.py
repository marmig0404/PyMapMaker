# database.py includes the class Database for use to connect to different databases
# as of right now, database.py only includes config for MySQL and PostgreSQL databases

import mysql.connector

import helpers


class Database(object):  # general database object format

    def __init__(self, host, port, dbname, username, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password
        self.isConnected = False


class MySQL(Database):  # class for mysql database used as an address database

    def connect(self):
        # connects to database using mysql connector
        helpers.write_to_log("Opening MySQL Session...")
        session = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.dbname,
            auth_plugin='mysql_native_password'
        )
        self.isConnected = session.is_connected()
        helpers.write_to_log("MySQL connection opened.")
        return session

    def __init__(self, host, port, dbname, username, password, table, address_column, last_modified_column):
        helpers.write_to_log("Initializing MySQL Database...")
        Database.__init__(self, host, port, dbname, username, password)
        self.address_column = address_column
        self.last_modified_column = last_modified_column
        self.table = table
        helpers.write_to_log("MySQL Database Initialized.")
        self.session = self.connect()

    def disconnect(self, silent=False):
        if silent:
            if self.isConnected:
                self.session.close()
        else:
            if self.isConnected:
                self.session.close()
                helpers.write_to_log("MySQL connection closed.")
            else:
                helpers.write_to_log("Attempted to close a MySQL connection that does not exist!")

    def __del__(self):
        self.disconnect(silent=True)
        pass

    def make_query(self, query):
        # general function to make a sql query
        cursor = self.session.cursor(buffered=True)
        response = cursor.execute(query, multi=True)
        return response

    def execute_command(self, command):
        # general function to execute a sql command
        cursor = self.session.cursor(buffered=True)
        cursor.execute(command)

    def get_column(self, column_name):
        # specific query to get a column from a table
        query = "SELECT %s FROM %s" % (column_name, self.table)
        return MySQL.make_query(self, query)

    def get_addresses(self):
        # pulls addresses from database, this part determines whether to update or create maps for all
        helpers.write_to_log("Attempting to pull addresses from address database.")
        # mode = helpers.get_config('General Config', 'Operation Mode')
        # if mode == "update":
        #     query = 'SELECT * FROM ' + self.table + ' WHERE ' + self.last_modified_column + ' >= ' \
        #             + helpers.last_run_time
        # elif mode == "all":
        #     query = 'SELECT * FROM ' + self.table
        # else:
        #     helpers.write_to_log("ERROR: Invalid Operation Mode, check config.ini.")
        #     sys.exit(2)
        query = 'SELECT ' + self.address_column + ',' + self.last_modified_column + ' FROM ' + self.table
        response = self.make_query(query)
        addresses = list()
        for result in response:
            if result.with_rows:
                for address in result.fetchall():
                    formatted_address = str(address[0]).replace('\r\n', ', ')
                    addresses.append(formatted_address)
        helpers.write_to_log("Sucessfully pulled addresses from address database.")
        return addresses


# class PGSQL(Database):  # class for postgresql database used as a map database
#
#     def __init__(self, host, port, dbname, username, password, schema, table_names, geometry_columns):
#         helpers.write_to_log("Initializing PostgreSQL Database...")
#         Database.__init__(self, host, port, dbname, username, password)
#         self.schema = schema
#         self.table_names = table_names
#         self.geometry_columns = geometry_columns
#         helpers.write_to_log("PostgreSQL Database Initialized.")
