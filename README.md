# hazard_detection
Raspberry Pi Zero W with sensor for detecting flood presence and (pump) not stupping malfunction. After detecting the problem, the notification is sent via e-mail.

## Description

The purpose is to avoid various hazards taking place to a techinical room. The premise is that in the room there are water tanks and there is electric water pump. We want to:
- detect the presence of water on ground level (a flood or leakage)
- detect a malfunction of the pump or the pressure switch that makes the pump to continously run (and in the end will burn out)

## Hardware

The brain consists of a Raspberry Pi Zero W, with internet connection.
The presence of water is detected by using a cheap ground humity sensor. 3 pins are used: Vcc, GND and DO (digital out: 1 or 0 when water level reaches a configured level - the adjustment is done by using the sensor's potentiometer)
<img src="ground_humidity_sensor.webp">
The motor malfunction is detected with the help of a microphone which can identify when the motor is running. The microphone used is digital, from Adafruit: I2S MEMS Microphone Breakout. The complete wiring and testing of the module: https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-test

## Requirements

First is to get the code from GitHub:
```
git clone https://github.com/Vlad-Mocanu/hazard_detection/
```
The following steps are optional, if you want to use virtualenv (instead of installing the package on system default):
```
virtualenv -p /usr/bin/python3 my_virt_env
source my_virt_env/bin/activate
python3 -m pip install --upgrade pip
```

To install the package and its dependencies, you can run:
```
pip3 install hazard_detection/
```

Note: The sound detection relies on pyAudio, which uses port_audio. A problem was with port_audio was encountered:
```
_portaudio.so: undefined symbol: Pa_GetStreamReadAvailable
```
To get around this https://stackoverflow.com/questions/36681836/pyaudio-could-not-import-portaudio/

## Usage

After you navigate to hazard_detection/hazard_detection, in order to run, you can use:
```
python3 hazard_detection.py
```

The default configuration file is hazard_detection/hazard_detection/hazard_config.json. This file can be edited to adjust the program to your needs. In order to use another configuration file, other than the default one you can run it like this:
```
python3 hazard_detection.py --config_file <path_to_config_file>
