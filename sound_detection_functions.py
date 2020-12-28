import pyaudio
import time
import numpy as np
import datetime

import water_detection

def logging_debug(message, logging):
    logging.debug("[%s] %s" % (datetime.datetime.now(), message))

def logging_info(message, logging):
    logging.info("[%s] %s" % (datetime.datetime.now(), message))

def get_recording_device(p, logging, config_options):
    logging_debug("Searching for recording device", logging)

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if (device_info.get('maxInputChannels') > 0):
            if ("snd_rpi_i2s_card" in device_info.get('name')):
                logging_debug("Will use device id %0d - %s" % (i, device_info.get('name')), logging)
                return i

def get_stream_from_recording_device(p, record_device_index, config_options):
    # stream object to get data from microphone
    stream = p.open(
        format = pyaudio.paInt32,
        channels = 1,
        rate = config_options["sound_detection"]["rate"],
        input = True,
        frames_per_buffer = config_options["sound_detection"]["chunk"],
        input_device_index = record_device_index
    )
    return stream

def detect_sound_from_chunk(data, logging, config_options):
    # convert data to integers, make np array
    data_int = np.frombuffer(data, np.int32)
    data_int = data_int[::2]
    data_int = np.array([abs(xi + config_options["sound_detection"]["calibration_offset"]) for xi in data_int])
    mean = np.mean(data_int)

    if (mean > config_options["sound_detection"]["chunk_treshold"]):
        logging_debug("Sound detected (mean: %d treashold: %d)" % (mean, config_options["sound_detection"]["chunk_treshold"]), logging)
        return 1
    else:
        return 0

def listen_for_duration(p, record_device_index, duration, logging, config_options):
    stream = get_stream_from_recording_device(p, record_device_index, config_options)

    logging_debug("Listening started (listen duration: %0d seconds)" % duration, logging)
    chunks_with_sound_detected = 0
    chunks_total = 0
    start_time = round(time.time())

    while round(time.time()) <= start_time + duration:
        # binary data
        data = stream.read(config_options["sound_detection"]["chunk"], exception_on_overflow = False)

        if detect_sound_from_chunk(data, logging, config_options):
            chunks_with_sound_detected = chunks_with_sound_detected + 1

        chunks_total = chunks_total + 1

    stream.stop_stream()
    stream.close()

    logging_debug("Chunks with sound detected %0d/%0d" % (chunks_with_sound_detected, chunks_total), logging)

    if (chunks_with_sound_detected / chunks_total > config_options["sound_detection"]["minute_treshold"]):
        return 1
    else:
        return 0

# function will exit after initial sound detection took place
def listen_until_sound_on(p, record_device_index, logging, config_options):
    while True:
        if listen_for_duration(p, record_device_index, config_options["sound_detection"]["listen_duration_per_minute"], logging, config_options):
            logging_debug("Initial sound detected", logging)
            return
        time.sleep(60 - config_options["sound_detection"]["listen_duration_per_minute"])

# function will exit after a minute does not have sound detected
def listen_until_sound_off(p, record_device_index, logging, config_options):
    consecutive_mins_with_sound = 0;

    while True:
        if listen_for_duration(p, record_device_index, 60, logging, config_options):
            consecutive_mins_with_sound = consecutive_mins_with_sound + 1
            logging_debug("Sound is still on after: %0d minutes" % consecutive_mins_with_sound, logging)
        else:
            if consecutive_mins_with_sound > 0:
                logging_info("Sound stopped after: %0d minutes" % consecutive_mins_with_sound, logging)
            return

        if (consecutive_mins_with_sound >= config_options["sound_detection"]["consecutive_listen_minutes"]):
            logging_info("Suspicious Sound detected!", logging)
            water_detection.sendEmail("Sound detection system: Suspicious Sound detected for over %0d minutes" % consecutive_mins_with_sound, logging, config_options)
