import paho.mqtt.client as mqtt
from google_project import settings
import json


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('esp8266/gps')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    print(str(msg.payload))
    # return(str(msg.payload))
    a = str(msg.payload)
    print("YEAH")
    print(a)
    dictionary = {
        "lat": float(a[2:11]),
        "lng": float(a[12:21])
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(r"C:\Users\ajinf\PycharmProjects\Maps\google\data.json", "w") as outfile:
        outfile.write(json_object)


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
print("EVEN HERE")
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
