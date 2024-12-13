import logging
import os
import subprocess
from time import sleep

import paho.mqtt.client as mqtt

log = logging.getLogger()

mqtt_url = os.environ['MQTT_URL']
mqtt_port = int(os.environ['MQTT_PORT'])

isOutputRetrieved = False

command = "cat ./sound/card*/pcm*/sub*/status | grep 'RUNNING'"


def retrieve_input():
    print("enable spoty input")
    try:
        send_message(0)
    except Exception as e:
        print(e)


def release_input():
    print("disable spoty input")
    try:
        send_message(1)
    except Exception as e:
        print(e)


def send_message(input):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="input_monitor", protocol=mqtt.MQTTv5)

    mqttc.connect(mqtt_url, mqtt_port)
    mqttc.loop_start()
    msg_info = mqttc.publish("/input", input, qos=0)
    log.info(f"Message is sent: {msg_info}")
    mqttc.disconnect()
    mqttc.loop_stop()


while True:
    try:
        console_output = subprocess.check_output(command, shell=True)
        console_output = console_output.decode("utf-8")
        if (console_output is None or console_output == "") and isOutputRetrieved:
            release_input()
            isOutputRetrieved = False
        elif (console_output is not None or console_output != "") and not isOutputRetrieved:
            retrieve_input()
            isOutputRetrieved = True
    except subprocess.CalledProcessError:
        if isOutputRetrieved:
            release_input()
            isOutputRetrieved = False
    sleep(1)
