# Project LAB
![image](https://user-images.githubusercontent.com/90660378/174719553-b6833969-b61c-4691-a317-2945dd0dfa05.png)

펌웨어 버전이 달라서 wificonnect가 안되는 오류가 발생 => 해결되는 대로 업데이트 예정

해결이 아직 안되어 이전에 배웠던 mqtt servo motor제어를 업로드

(블럭도)
![image](https://user-images.githubusercontent.com/90660378/175207787-76898bba-db6d-4a03-831f-307522e50118.png)



코드 1(ultrasonic_publish.py)
import random
import time
import paho.mqtt.client as mqtt_client
import RPi.GPIO as GPIO                     # GPIO 라이브러리 모듈 import
import time                                 # 시간 관련 라이브러리 모듈 import

# broker 정보 #1
broker_address = "192.168.0.185"
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

    # client 생성 #2
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    # 콜백 함수 설정 #3
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    # broker 연결 #4
    client.connect(host=broker_address, port=broker_port)
    return client

TRIG_PIN = 20                               # Trig 핀 지정
ECHO_PIN = 21                               # Echo 핀 지정

def initUltrasonic():                       # 초음파 센서 초기화 함수
 GPIO.setup(TRIG_PIN, GPIO.OUT)             # Trig 핀 출력 설정
 GPIO.setup(ECHO_PIN, GPIO.IN)              # Echo 핀 출력 설정

def controlUltrasonic():                    # 초음파 센서 제어 함수
    distance = 0.0                          # 거리 변수 선언
    GPIO.output(TRIG_PIN, False)            # Trig 핀 LOW 신호 출력
    time.sleep(0.5)                         # 500ms 지연
    GPIO.output(TRIG_PIN, True)             # Trig 핀 HIGH 신호 출력
    time.sleep(0.00001)                     # 10us 지연
    GPIO.output(TRIG_PIN, False)            # Trig 핀 LOW 신호 출력
    
    while GPIO.input(ECHO_PIN) == 0 :       # Echo 핀 신호 입력 대기
        pulse_start = time.time()           # 대기 시작 시간 측정
    while GPIO.input(ECHO_PIN) == 1 :       # Echo 핀 신호 입력
        pulse_end = time.time()             # 입력 시간 측정
    
    pulse_duration = pulse_end - pulse_start # 시간차 계산
    distance = pulse_duration * 17000        # 거리 계산
    distance = round(distance, 2)
    return distance 

def publish(client: mqtt_client):

    GPIO.setmode(GPIO.BCM)                      # GPIO 모드 설정
    distance = 0.0                              # 거리 변수 설정
    initUltrasonic()                            # 초음파 센서 초기화
    print("Ultrasonic Operating ...") 

    while True:
        time.sleep(1)
        distance = controlUltrasonic()      # 거리 측정
        msg = distance
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` cm  to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start() #5
    print(f"connect to broker {broker_address}:{broker_port}")
    publish(client) #6

if __name__ == '__main__':
    run()
    
코드2(servo.py)
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
