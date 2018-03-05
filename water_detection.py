#!/usr/bin/python
import RPi.GPIO as GPIO
import smtplib
import time
import datetime
import logging

channel = 17

smtp_host = 'smtp.gmail.com'
smtp_port = 465
smtp_user = 'my_test@gmail.com'  
smtp_password = 'my_password'

smtp_receivers = ['my_mail@gmail.com']  
smtp_subject_flood = 'APA DETECTATA'
smtp_subject_ok = 'Totul e OK'
smtp_subject_normal = 'Alarma inundatie: '
smtp_subject_online = 'Detectie inundatie online: '

log_filename = 'water_detection.log'
log_level = logging.INFO

email_header = """From: Alarma Inundatie <%s>  
To: %s  
Subject: """ % (smtp_user, ", ".join(smtp_receivers))

def sendEmail(smtp_message):
	now = "[%s]" % datetime.datetime.now()
	try:
		server = smtplib.SMTP_SSL(smtp_host, smtp_port)
		server.ehlo()
		server.login(smtp_user, smtp_password)
		server.sendmail(smtp_user, smtp_receivers, smtp_message)
		server.close()
		
		print now + 'Email sent!'
		logging.info(now + 'Email sent!')
	except:
		print now + 'Email not sent!'
		logging.error(now + 'Email not sent!')
		
def get_flood_status(channel, email_subject_prefix):
	now = "[%s]" % datetime.datetime.now()
	
	if GPIO.input(channel):
		print now + smtp_subject_ok
		logging.info(now + smtp_subject_ok)
		sendEmail(email_header + email_subject_prefix + smtp_subject_ok)
	else:
		print now + smtp_subject_flood
		logging.info(now + smtp_subject_flood)
		sendEmail(email_header + email_subject_prefix + smtp_subject_flood)

def callback(channel):
	get_flood_status(channel, smtp_subject_normal)
	
logging.basicConfig(filename=log_filename, level=log_level)
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

GPIO.add_event_detect(channel, GPIO.BOTH, callback, bouncetime=1000)

get_flood_status(channel, smtp_subject_online)

while True:
	time.sleep(1000)
