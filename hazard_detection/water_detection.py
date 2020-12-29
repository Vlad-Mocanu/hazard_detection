import smtplib
import time
import datetime

smtp_receivers = ['my_mail@gmail.com']
smtp_subject_flood = 'APA DETECTATA'
smtp_subject_ok = 'Totul e OK'

def sendEmail(smtp_message, logging, config_options):
    now = "[%s] " % datetime.datetime.now()
    email_header = """From: Alarma Inundatie <%s>
To: %s
Subject: """ % (config_options["mail"]["smtp_user"], ", ".join(config_options["mail"]["smtp_receivers"]))

    try:
        server = smtplib.SMTP_SSL(config_options["mail"]["smtp_host"], config_options["mail"]["smtp_port"])
        server.ehlo()
        server.login(config_options["mail"]["smtp_user"], config_options["mail"]["smtp_password"])
        server.sendmail(config_options["mail"]["smtp_user"], config_options["mail"]["smtp_receivers"], email_header + smtp_message)
        server.close()

        logging.info(now + "Email sent!")
    except:
        logging.error(now + "Email NOT sent!")

def get_flood_status(pin_value, email_subject_prefix, logging, config_options):
    now = "[%s] " % datetime.datetime.now()

    if pin_value:
        logging.info(now + smtp_subject_ok)
        sendEmail(email_subject_prefix + smtp_subject_ok, logging, config_options)
    else:
        logging.info(now + smtp_subject_flood)
        sendEmail(email_subject_prefix + smtp_subject_flood, logging, config_options)
