from umqtt.simple import MQTTClient

# Test reception e.g. with:
# mosquitto_sub -t foo_topic


def main(server="192.168.0.2"):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(b"shed", b"hello")
    c.disconnect()


if __name__ == "__main__":
    main()
