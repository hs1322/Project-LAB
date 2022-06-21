'''
实验名称：MQTT通信
版本：v1.0
日期：2019.8
作者：01Studio
说明：编程实现MQTT通信，实现发布数据。
'''
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

        #串口打印信息
        print('network information:', wlan.ifconfig())

        return True    

#发布数据任务
def MQTT_Send(tim):
    global step1
    client.publish(TOPIC, 'Hello 01Studio!'+str(step1))
    step1 = step1 +1
    print(step1)

#执行WIFI连接函数并判断是否已经连接成功
if WIFI_Connect():
    SERVER = '192.168.0.2'
    PORT = 1883
    CLIENT_ID = '01Studio-ESP32' # 客户端ID
    TOPIC = 'temp1' # TOPIC名称
    client = MQTTClient(CLIENT_ID, SERVER, PORT)
    client.connect()

    #开启RTOS定时器，编号为-1,周期1000ms，执行socket通信接收任务
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)
