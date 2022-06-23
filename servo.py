import sys
import time
from pymata4 import pymata4
import paho.mqtt.client as mqtt_client
import RPi.GPIO as GPIO
import random

board = pymata4.Pymata4()

servo = board.set_pin_mode_servo(11) # 11번핀을 서보모터 신호선으로 설정


def move_servo(v):                  # 파이선 함수 정의
    board.servo_write(11, v)
    time.sleep(1) 


broker_address = "localhost"
broker_port = 1883

topic = "distance"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else:
            print(f"Failed to connect, Returned code: {rc}")

    def on_disconnect(client, userdata, flags, rc=0):
        print(f"disconnected result code {str(rc)}")

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    # client 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결
    client.connect(host=broker_address, port=broker_port)
    return client



def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        num = float(msg.payload.decode())
        if num >= 180:
            num = 180
            move_servo(int(num))
        else :
            move_servo(int(num))
    

    client.subscribe(topic) #1
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
