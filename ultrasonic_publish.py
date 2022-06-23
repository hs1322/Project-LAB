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