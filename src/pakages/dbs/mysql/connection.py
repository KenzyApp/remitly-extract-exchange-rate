#!/usr/bin/python
# -*- coding: utf-8 -*-



import sys

from mysql.connector import MySQLConnection, Error

if sys.version_info[0] == 2:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser





def readDatabaseConfig(filename='./path/to/file.ini', section='mysql'):

    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """

    try:
		# create parser and read ini configuration file
		parser = ConfigParser()
		parser.read(filename)

		# get section, default to mysql
		db = {}

		if parser.has_section(section):
			items = parser.items(section)
			for item in items:
				db[item[0]] = item[1]
		else:
			raise Exception('{0} not found in the {1} file'.format(section, filename))

    except Error as error:
        print error

    else:
		return db


    return None





def connectDatabase(db_config=None):
    """ Connect to MySQL database """

    try:
        print 'Connecting to MySQL database...'
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print 'connection established.'
        else:
            print 'connection failed.'

    except Error as error:
        print error

    else:
        return conn
        print 'Return connection.'


    return None







def closeDatabase(conn=None):
    """ Connect to MySQL database """

    try:
        conn.close()
        print "Connection closed."

    except Error as error:
        print error




