#!/usr/bin/python3
import argparse
import json
import pyaudio
import time
import logging
import RPi.GPIO as GPIO
import datetime
import sched
import threading

import mail_functions
import sound_detection_functions
import water_detection_functions

# read configuration
parser = argparse.ArgumentParser()
parser.add_argument("--config_file", "-f", default="hazard_config.json", help="path to configuration json file (default: hazard_config.json)")
args = parser.parse_args()

with open(args.config_file) as data_file:
    config_options = json.load(data_file)
data_file.close()


# configure loggers
handlers = [logging.FileHandler(config_options["logging"]["log_file"]), logging.StreamHandler()]
logging.basicConfig(level = config_options["logging"]["level"], handlers = handlers, format = "[%(asctime)-15s] %(message)s")

# schedule the next status report
s = sched.scheduler(time.time, time.sleep)
status_thread = threading.Thread(target = mail_functions.schedule_next_status, args = (1, s, logging, config_options))
status_thread.start()

# add callback for water detection - each time the pin changes it will trigger the callback and send mail
def callback(channel):
    water_detection_functions.get_flood_status(GPIO.input(channel), "", logging, config_options)

# water #######################
if config_options["water_detection"]["enable_function"]:
    logging.info("Water detection function enabled")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config_options["water_detection"]["channel"], GPIO.IN)

    GPIO.add_event_detect(config_options["water_detection"]["channel"], GPIO.BOTH, callback, bouncetime=config_options["water_detection"]["bouncetime"])
else:
    logging.info("Water detection function not enabled (see config)")

# sound #######################
if config_options["sound_detection"]["enable_function"]:
    # initialize sound detection and determine the correct hardware used
    logging.info("Sound detection function enabled")
    logging.info("Initialize PyAudio...")
    p = pyaudio.PyAudio()

    record_device_index = sound_detection_functions.get_recording_device(p, logging, config_options)

    # sound detection
    while True:
        sound_detection_functions.listen_until_sound_on(p, record_device_index, logging, config_options)
        sound_detection_functions.listen_until_sound_off(p, record_device_index, logging, config_options)
else:
    logging.info("Sound detection function not enabled (see config)")

