import json
import subprocess
from time import sleep

from websocket import create_connection

isOutputRetrieved = False

command = "cat /proc/asound/card*/pcm*/sub*/status | grep 'RUNNING'"


def retrieve_input():
    print("enable spoty input")
    try:
        ws = create_connection("ws://127.0.0.1:8000/ws")
        json_data = json.loads(ws.recv())
        if json_data['input'] != 0:
            json_data['input'] = 0
        ws.send(json.dumps(json_data))
        ws.close()
    except Exception as e:
        print(e)


def release_input():
    print("disable spoty input")
    try:
        ws = create_connection("ws://127.0.0.1:8000/ws")
        json_data = json.loads(ws.recv())
        json_data['input'] = 1
        ws.send(json.dumps(json_data))
        ws.close()
    except Exception as e:
        print(e)


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


