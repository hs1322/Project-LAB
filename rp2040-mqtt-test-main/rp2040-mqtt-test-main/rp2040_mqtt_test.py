import network,time
from simple import MQTTClient #导入MQTT板块
from machine import I2C,Pin,Timer

step1 = 0

def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('iptime_shkim_24', 'ksh89377') #输入WIFI账号密码
        
    if wlan.isconnected():
        print('network information:', wlan.ifconfig())
        return True    

def MQTT_Send(tim):
    global step1
    client.publish(TOPIC, 'Hello broker'+str(step1))
    step1 = step1 +1
    print(step1)

if WIFI_Connect():
    SERVER = '192.168.0.2'   // my rapa ip address , mqtt broker가 실행되고 있음
    PORT = 1883
    CLIENT_ID = 'sungho-Kim' # clinet id 이름
    TOPIC = 'temp1' # TOPIC 이름
    client = MQTTClient(CLIENT_ID, SERVER, PORT)
    client.connect()

    #开启RTOS定时器，编号为-1,周期1000ms，执行socket通信接收任务
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)
