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
from ssd1306 import SSD1306_I2C
import dht

#初始化相关模块
i2c = I2C(sda=Pin(13), scl=Pin(14))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
step1 = 0
d = dht.DHT11(Pin(27)) #传感器连接到引脚15
time.sleep(1)   #首次启动停顿1秒让传感器稳定
#WIFI连接函数
def WIFI_Connect():

    WIFI_LED=Pin(2, Pin.OUT) #初始化WIFI指示灯

    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('iptime_shkim_24', 'ksh89377') #输入WIFI账号密码

        while not wlan.isconnected():

            #LED闪烁提示
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

            #超时判断,15秒没连接成功判定为超时
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():
        #LED点亮
        WIFI_LED.value(1)

        #串口打印信息
        print('network information:', wlan.ifconfig())

        #OLED数据显示（如果没接OLED，请将下面代码屏蔽）
        oled.fill(0)   #清屏背景黑色
        oled.text('IP/Subnet/GW:',0,0)
        oled.text(wlan.ifconfig()[0], 0, 20)
        oled.text(wlan.ifconfig()[1],0,38)
        oled.text(wlan.ifconfig()[2],0,56)
        oled.show()
        return True

    else:
        return False

#发布数据任务
def MQTT_Send(tim):
    d.measure()         #温湿度采集

   #OLED显示温湿度
    oled.fill(0) #清屏背景黑色
    oled.text('01Studio', 0, 0)
    oled.text('DHT11 test:',0,15)
    oled.text(str(d.temperature() )+' C',0,40)   #温度显示
    oled.text(str(d.humidity())+' %',48,40)  #湿度显示
    oled.show()
    #client.check_msg()
    #global step1
    client.publish(TOPIC, str(d.temperature()))
    #step1 = step1 +1

#执行WIFI连接函数并判断是否已经连接成功
if WIFI_Connect():

    SERVER = '192.168.0.2'
    PORT = 1883
    CLIENT_ID = '01Studio-ESP32' # 客户端ID
    TOPIC = 'temp' # TOPIC名称
    client = MQTTClient(CLIENT_ID, SERVER, PORT)
    client.connect()

    #开启RTOS定时器，编号为-1,周期1000ms，执行socket通信接收任务
    tim = Timer(-1)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)
