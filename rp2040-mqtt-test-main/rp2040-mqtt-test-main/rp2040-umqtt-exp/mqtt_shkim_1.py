from umqtt.simple import MQTTClient
#import dht
import ubinascii
import machine
import network
from time import sleep, sleep_ms
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.active(True)
        wlan.connect('iptime_shkim_24', 'ksh89377')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

#d = dht.DHT11(machine.Pin(4))
#d.measure()
#pin=machine.Pin(2,machine.Pin.OUT)
client_id="192.168.1.6"
broker_id="192.168.0.2"
TOPIC1=b"Hello_Msg"
def clientpublish(server=broker_id, topic=b"/foo", data=None):
    sleep_ms(200)
    c = MQTTClient(client_id, server)
    c.connect()
    sleep_ms(200)
    c.publish(topic, data)
    sleep_ms(200)
    c.disconnect()
       

def main():
    do_connect()
    while True:
        
        clientpublish(broker_id,TOPIC1,b"Hello")
if __name__=="__main__":
    main()
