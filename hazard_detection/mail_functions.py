

import smtplib
import time
import datetime

import water_detection_functions

#functions related to status sending ################
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_delay_until_next_status():
    now = datetime.datetime.now()
    d = datetime.datetime(now.year, now.month, now.day, 12, 0, 0)
    next_status_date = next_weekday(d, 7) # 0 = Monday, 1=Tuesday, 2=Wednesday...

    my_delay = next_status_date - now
    return my_delay.total_seconds()

def schedule_next_status(send_now, sched, logging, config_options):
    if send_now == 1:
        wait_delay = 0
    else:
        wait_delay = get_delay_until_next_status()
    sched.enter(wait_delay, 1, perform_action_on_sched, (send_now, sched, logging, config_options))

    logging.info("Scheduled status send after %d seconds" % wait_delay)

    sched.run()

def perform_action_on_sched(send_now, sched, logging, config_options):
    if send_now == 1:
        subject_prefix = "System restarted: "
    else:
        subject_prefix = "Report: "
    water_detection_functions.get_flood_status(config_options["water_detection"]["channel"], subject_prefix, logging, config_options)
    schedule_next_status(0, sched, logging, config_options)

# functions related to sending email ################
def sendEmail(smtp_message, logging, config_options):
    email_header = """From: Alarma Inundatie <%s>
To: %s
Subject: """ % (config_options["mail"]["smtp_user"], ", ".join(config_options["mail"]["smtp_receivers"]))

    logging.info(smtp_message)
    try:
        server = smtplib.SMTP_SSL(config_options["mail"]["smtp_host"], config_options["mail"]["smtp_port"])
        server.ehlo()
        server.login(config_options["mail"]["smtp_user"], config_options["mail"]["smtp_password"])
        server.sendmail(config_options["mail"]["smtp_user"], config_options["mail"]["smtp_receivers"], "%s %s - %s" % (email_header, smtp_message, datetime.datetime.now()))
        server.close()

        logging.info("Email sent!")
    except:
        logging.error("Email NOT sent!")
