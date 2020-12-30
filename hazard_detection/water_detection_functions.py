import smtplib
import time
import datetime

import mail_functions

def get_flood_status(pin_value, email_subject_prefix, logging, config_options):
    now = "[%s] " % datetime.datetime.now()

    if pin_value:
        mail_functions.sendEmail(email_subject_prefix + "Everything OK", logging, config_options)
    else:
        mail_functions.sendEmail(email_subject_prefix + "WATER DETECTED", logging, config_options)
