#!/usr/bin/python
# -*- coding: utf-8 -*-

# Cron: /home4/rovisof1/python/bin/python2.7 /home4/rovisof1/public_html/project/remitly/__init__.py



# Python modules

import os
import re
import socket
import pycurl

import smtplib
from email.mime.text import MIMEText

import operator

from datetime import datetime, timedelta
from time import gmtime, strftime
from pytz import timezone


from pakages.dbs.mysql.connection import *
#~ import pakages.dbs.mysql.connection







if __name__ == "__main__":
	print '\n\n'
	print "REMITLY :: GET MXN CURRENCY CONVERTION"
	print "--------------------------------------------------------"


	urlStr = "https://www.remitly.com/us/en/mexico"
	dirPath = os.path.dirname( os.path.abspath( __file__ ) )
	configFile = dirPath + "/config/db.ini"


	hostnameServerStr = socket.gethostname()
	databaseConfigSelector = 'mysql-external-connection'

	if hostnameServerStr == 'rsj25.rhostjh.com':
		databaseConfigSelector = 'mysql-release'


	sendNotificationMail = True
	sendNotificationUSDOver = 22.00
	sendNotificationUSDUnder = 19.00
	sendNotificationMailToIsrael = True
	sendNotificationMailToJorge = True

	#~ isAppInProduction = False
	isAppInProduction = True

	smtpServer = 'mail.rovisoft.net'
	smtpFromAddr = 'contact@rovisoft.net'
	smtpFromPass = '8.usQW$TdP_h>'







	print ""
	print ""
	print "Get web page: ", urlStr
	print ""

	resourcesDirectory = dirPath + '/resources/'

	if not os.path.exists( resourcesDirectory ):
		os.makedirs( resourcesDirectory )

	savedFileStr = dirPath + '/resources/rate.html'

	if isAppInProduction == True:
		c = pycurl.Curl()
		c.setopt( pycurl.FOLLOWLOCATION, True )
		c.setopt( pycurl.URL, urlStr )
		c.setopt( pycurl.USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36' )
		c.setopt( pycurl.ENCODING, "gzip,deflate" )

		with open( savedFileStr, 'w' ) as f:
			c.setopt( c.WRITEFUNCTION, f.write )
			c.perform()
		c.close()







	print ""
	print ""
	print ""
	print "Convert USD to MXN, check the file: ", savedFileStr
	print ""

	f = open( savedFileStr, 'r' )
	getFileStr = f.read()
	f.close()

	#~ getMxnRatePattern = re.compile( '<b class="rate">(.*)</b>' )
	getMxnRatePattern = re.compile( '</span> Remitly Everyday: <span style="color:#42D4B0">(.*)</span>' )
	getMxnRateStr = re.findall( getMxnRatePattern, getFileStr )[0]
	print "getMxnRateStr: ", getMxnRateStr

	getMxnCurrencyPattern = re.compile( '<span class="currency">(.*)</span>' )
	getMxnCurrencyStr = re.findall( getMxnCurrencyPattern, getFileStr )[0]
	print "getMxnCurrencyStr: ", getMxnCurrencyStr







	print ""
	print ""
	print ""
	print "Send email if the sendNotificationMail is true, right now is: ", sendNotificationMail
	print ""

	if sendNotificationMail == True and isAppInProduction == True:
		smtpTimeNow = strftime('%Y-%m-%d %H:%M:%S', gmtime())

		smtpInfo = {}
		smtpInfo['Subject'] = 'Remitly: USD = '+getMxnRateStr+' MX ---'+smtpTimeNow+' #RoviSoft.net'
		smtpInfo['From'] = '"RoviSoft.net" <contact@rovisoft.net>'
		smtpInfo['Reply-To'] = '"RoviSoft.net" <admin@rovisoft.net>'
		smtpInfo['Body'] = 'https://project.rovisoft.net/remitly/\nThanks!'

		smtpCharset = 'utf-8'
		smtpContentMIMEType = 'plain'

		smtpMessage = MIMEText(smtpInfo['Body'].encode(smtpCharset), smtpContentMIMEType, smtpCharset)
		smtpMessage['From'] = smtpInfo['From']
		smtpMessage['Reply-To'] = smtpInfo['Reply-To']
		smtpMessage['Subject'] = smtpInfo['Subject']


		if sendNotificationMailToIsrael == True and float(getMxnRateStr) >= sendNotificationUSDOver or float(getMxnRateStr) <= sendNotificationUSDUnder:
			print 'sendNotificationUSDOver: %s' % str(sendNotificationUSDOver)
			print 'sendNotificationUSDUnder: %s' % str(sendNotificationUSDUnder)

			smtpInfo['To'] = ['"Israel Roldan" <israel.alberto.rv@gmail.com>']
			smtpMessage['To'] = ', '.join(smtpInfo['To'])

			print smtpMessage.as_string()
			print '-----------------------------------------------------------------'

			try:
				sendEmail = smtplib.SMTP_SSL(smtpServer)
				sendEmail.login(smtpFromAddr, smtpFromPass)
				sendEmail.sendmail(smtpInfo['From'], smtpInfo['To'], smtpMessage.as_string())
			except:
				print 'Unexpected error:', sys.exc_info()[0]
				raise
			else:
				print 'The email was sended successful!'
				sendEmail.quit()


		jorgeDuqueSendNotificationUSDOver = 22.00

		if sendNotificationMailToJorge == True and float(getMxnRateStr) >= jorgeDuqueSendNotificationUSDOver:
			print 'sendNotificationUSDOver: %s' % str(jorgeDuqueSendNotificationUSDOver)

			smtpInfo['To'] = ['"Jorge Duque" <jorgeduque71@gmail.com']
			smtpMessage['To'] = ', '.join(smtpInfo['To'])

			print smtpMessage.as_string()
			print '-----------------------------------------------------------------'

			try:
				sendEmail = smtplib.SMTP_SSL(smtpServer)
				sendEmail.login(smtpFromAddr, smtpFromPass)
				sendEmail.sendmail(smtpInfo['From'], smtpInfo['To'], smtpMessage.as_string())
			except:
				print 'Unexpected error:', sys.exc_info()[0]
				raise
			else:
				print 'The email was sended successful!'
				sendEmail.quit()







	print ""
	print ""
	print ""
	print "Connecting to the database..."
	print ""

	datetimeFormatStart = '%Y-%m-%d 00:00:00'
	datetimeFormatEnd = '%Y-%m-%d 23:59:59'

	try:
		dbConfig = readDatabaseConfig( configFile, databaseConfigSelector )
		print "dbConfig Host: ", dbConfig['host']
		print "dbConfig DB's: ", dbConfig['database']

	except Error as error:
		print error

	finally:
		if dbConfig == None:
			exit()


	try:
		dbConn = connectDatabase( dbConfig )
		#~ print "dbConn: ", dbConn

	except Error as error:
		print error

	finally:
		if dbConn == None:
			exit()







	print ""
	print ""
	print ""
	print "Saving information in database..."
	print ""

	#~ fmt = "%Y-%m-%d %H:%M:%S %Z%z"
	fmt = "%Y-%m-%d %H:%M:%S"
	timezoneUtc = datetime.now( timezone( 'UTC' ) )
	timezoneUtcStr = timezoneUtc.strftime( fmt )

	if isAppInProduction == True:
		query = "INSERT INTO currency_usd_to ( id, ammount, datetime, currency_id, timezone_id ) VALUES (%s, %s, %s, %s, %s );"
		queryArgs = ( None, getMxnRateStr, timezoneUtcStr, 1, 1 )

		try:
			dbCursor = dbConn.cursor()
			dbCursor.execute( query, queryArgs )

			if dbCursor.lastrowid:
				None
				#~ print 'Table currency_usd_to. Insert ID: ', dbCursor.lastrowid
			else:
				print 'Error: Somthing was wrong with the Insert.'

			dbConn.commit()

		except Error as error:
			print error
			dbCursor.close()
			closeDatabase( dbConn )
			exit()

		finally:
			dbCursor.close()









	print ""
	print ""
	print ""
	print "Making report's tables in database..."
	print ""

	query = "SELECT datetime FROM currency_usd_to WHERE id = 1;"

	try:
		dbCursor = dbConn.cursor()
		dbCursor.execute( query )

		firstRecordDB = dbCursor.fetchone()

	except Error as error:
		print error
		dbCursor.close()
		closeDatabase( dbConn )
		exit()

	finally:
		dbCursor.close()


	query = "SELECT datetime, ammount FROM currency_usd_to WHERE id = ( SELECT COUNT(id) FROM currency_usd_to );"

	try:
		dbCursor = dbConn.cursor()
		dbCursor.execute( query )

		lastRecordDB = dbCursor.fetchone()

	except Error as error:
		print error
		dbCursor.close()
		closeDatabase( dbConn )
		exit()

	finally:
		dbCursor.close()


	firstRecord = firstRecordDB[0]
	lastRecord = lastRecordDB[0]
	lastAmmountRecord = lastRecordDB[1]

	firstRecordStr = firstRecord.strftime( datetimeFormatStart )
	lastRecordStr = lastRecord.strftime( datetimeFormatStart )







	print ""
	print ""
	print ""
	print "Report per day..."
	print ""

	query = "SELECT datetime FROM report_per_day WHERE id = ( SELECT COUNT(id) FROM report_per_day );"

	try:
		dbCursor = dbConn.cursor()
		dbCursor.execute( query )

		lastRecordPerDay = dbCursor.fetchone()

	except Error as error:
		print error
		closeDatabase( dbConn )
		exit()


	if lastRecordPerDay == None:
		lastRecordPerDay = firstRecord
	else:
		lastRecordPerDay = lastRecordPerDay[0] + timedelta(1)

	lastRecordPerDayStr = lastRecordPerDay.strftime( datetimeFormatStart )


	while lastRecordPerDay < datetime( lastRecord.year, lastRecord.month, lastRecord.day ):
		lastRecordPerDayStartStr = lastRecordPerDay.strftime( datetimeFormatStart )
		lastRecordPerDayEndStr = lastRecordPerDay.strftime( datetimeFormatEnd )

		query = "SELECT * FROM currency_usd_to WHERE datetime >= %s AND datetime <= %s;"
		queryArgs = ( lastRecordPerDayStartStr, lastRecordPerDayEndStr )

		try:
			dbCursor = dbConn.cursor()
			dbCursor.execute( query, queryArgs )

			data = dbCursor.fetchall()

		except Error as error:
			print error
			closeDatabase( dbConn )
			exit()


		dateDictionary = {}
		average = 0
		highest = 0
		lowest = 0
		constant = 0
		totalResults = len( data )

		if (totalResults > 0):
			for dateArray in data:
				average += dateArray[1]
				ammount = str(dateArray[1])
				dateDictionary[ammount] = dateDictionary.get( ammount, 0 ) + 1

			average = "%.2f" % (average / totalResults )
			highest = max(dateDictionary.keys(), key=float)
			lowest = min(dateDictionary.keys(), key=float)
			constant = max(dateDictionary.iteritems(), key=operator.itemgetter(1))[0]

		del data


		if isAppInProduction == True:
			query = "INSERT INTO report_per_day ( id, datetime, average, highest, lowest, constant ) VALUES (%s, %s, %s, %s, %s, %s );"
			queryArgs = ( None, lastRecordPerDayStartStr, average, highest, lowest, constant )

			#~ print 'Insert %s: [average: %s, highest: %s, lowest: %s, constant: %s]' % ( lastRecordPerDayStartStr[:10], average, highest, lowest, constant )

			try:
				dbCursor = dbConn.cursor()
				dbCursor.execute( query, queryArgs )

				if not dbCursor.lastrowid:
					print 'Error: Somthing was wrong with the Insert. Day: ' % ( lastRecordPerDayStartStr[:10] )

				dbConn.commit()

			except Error as error:
				print error
				dbCursor.close()
				closeDatabase( dbConn )
				exit()

			finally:
				dbCursor.close()

		del dateDictionary
		lastRecordPerDay += timedelta(1)







	print ""
	print ""
	print ""
	print "Create JS file with all statistics..."
	print ""

	query = "SELECT datetime, average, highest, lowest, constant FROM report_per_day WHERE 1;"

	try:
		dbCursor = dbConn.cursor()
		dbCursor.execute( query )

		allRecordsPerDay = dbCursor.fetchall()

	except Error as error:
		print error
		closeDatabase( dbConn )
		exit()


	jsArrayDirectory = dirPath + '/resources/jsArray/'

	if not os.path.exists( jsArrayDirectory ):
		os.makedirs( jsArrayDirectory )

	jsArrayFilePath = dirPath + '/resources/jsArray/perDay.js'
	jsArrayFile = open( jsArrayFilePath, 'w' )
	fileContent = 'var jsArrayPerDay = ['

	for record in allRecordsPerDay:
		datetimeYearRecord = str(record[0].year)
		datetimeMonthRecord = str(record[0].month-1)
		datetimeDayRecord = str(record[0].day)
		averageRecord = str(record[1])
		highestRecord = str(record[2])
		lowestRecord = str(record[3])
		# constantRecord = str(record[4])

		fileContent += '[new Date(%s, %s, %s),%s,%s,%s],' % ( datetimeYearRecord, datetimeMonthRecord, datetimeDayRecord, averageRecord, highestRecord, lowestRecord )

	fileContent = fileContent[:-1]
	fileContent += '];'

	jsArrayFile.write( fileContent )
	jsArrayFile.close()







	print ""
	print ""
	print ""
	print "Report today..."
	print ""

	lastRecordToday = lastRecord
	lastRecordTodayStartStr = lastRecordToday.strftime( datetimeFormatStart )
	lastRecordTodayEndStr = lastRecordToday.strftime( datetimeFormatEnd )

	query = "SELECT * FROM currency_usd_to WHERE datetime >= %s AND datetime <= %s;"
	queryArgs = ( lastRecordTodayStartStr, lastRecordTodayEndStr )

	try:
		dbCursor = dbConn.cursor()
		dbCursor.execute( query, queryArgs )

		data = dbCursor.fetchall()

	except Error as error:
		print error
		closeDatabase( dbConn )
		exit()


	dateDictionary = {}
	average = 0
	highest = 0
	lowest = 0
	constant = 0
	totalResults = len( data )

	if (totalResults > 0):
		for dateArray in data:
			average += dateArray[1]
			ammount = str(dateArray[1])
			dateDictionary[ammount] = dateDictionary.get( ammount, 0 ) + 1

		average = "%.2f" % (average / totalResults )
		highest = max(dateDictionary.keys(), key=float)
		lowest = min(dateDictionary.keys(), key=float)
		constant = max(dateDictionary.iteritems(), key=operator.itemgetter(1))[0]

	#~ print 'totalResults: ', totalResults
	#~ print 'average: ', average
	#~ print 'highest: ', highest
	#~ print 'lowest: ', lowest
	#~ print 'constant: ', constant


	jsArrayDirectory = dirPath + '/resources/jsArray/'

	if not os.path.exists( jsArrayDirectory ):
		os.makedirs( jsArrayDirectory )

	jsArrayFilePath = dirPath + '/resources/jsArray/today.js'
	jsArrayFile = open( jsArrayFilePath, 'w' )

	lastAmmountRecordStr = str(lastAmmountRecord)
	totalResultsStr = str(totalResults)
	datetimeTodayStr = str(lastRecordToday) + ' UTC'
	averageStr = str(average)
	highestStr = str(highest)
	lowestStr = str(lowest)
	constantStr = str(constant)

	fileContent = 'var jsObjectToday = {todayDatetime: "%s", todayAmmount: "%s", todayAverage: "%s", todayHighest: "%s", todayLowest: "%s", todayConstant: "%s", todayTotalResults: "%s"}' % ( datetimeTodayStr, lastAmmountRecordStr, averageStr, highestStr, lowestStr, constantStr, totalResultsStr )

	jsArrayFile.write( fileContent )
	jsArrayFile.close()







	print ""
	print ""
	print ""
	print "Close connection to the database..."

	closeDatabase( dbConn )







	print ""
	print ""
	print ""
	print "--------------------------------------------------------"
	print "REMITLY :: JUST FINISHED"
	print '\n\n\n'






