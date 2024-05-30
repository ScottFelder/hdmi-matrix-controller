from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig

from hdmi_matrix import HdmiMatrix, Power
import socket
import os

# https://pypi.org/project/fastapi-mqtt/
# https://sabuhish.github.io/fastapi-mqtt/

app = FastAPI()

mqtt_config = MQTTConfig(host="192.168.110.201",
                         port=1883,
                         keepalive=60)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


s = socket.socket()

host = os.environ["HOST"]
port = os.environ["PORT"] = "8000"
print("Host: " + host)
print("Port: " + port)
s.connect((host, int(port)))

io = os.environ["IO"].split("x")
print(os.environ["IO"])

matrix = HdmiMatrix(io[0], io[1], s)


@app.get("/")
async def root():
    mqtt.publish("/mqtt", "Hdmi Matrix Controller")  # publishing mqtt topic
    return {"message": "Hdmi Matrix Controller"}


@app.get("/power")
async def power():
    ret = matrix.exec_command(matrix.Read_Power)
    return {"power": ret}


@app.get("/power/{z}")
async def power(z: Power):
    ret = matrix.exec_command(matrix.Set_Power.format(z.value))
    return {"power": ret}


@app.get("/system/link_in/{x}")
async def system_link_in(x: int):
    ret = matrix.exec_command(matrix.Read_Link_In.format(x))
    return {"Link In": ret}


@app.get("/map/input/{x}/output/{y}")
async def map_input(x: int, y: int):
    ret = matrix.exec_command(matrix.Set_In_AV_Out.format(x, y))
    return {"Map Input": ret}


@app.get("/swap/{y1}/{y2}")
async def swap_output(y1: int, y2: int):
    out1 = matrix.exec_command(matrix.Read_AV_Out.format(y1)).strip("AV").strip("\r\n").split("->")
    out2 = matrix.exec_command(matrix.Read_AV_Out.format(y2)).strip("AV").strip("\r\n").split("->")
    matrix.exec_command(matrix.Set_In_AV_Out.format(out1[0].strip(), out2[1].strip()))
    matrix.exec_command(matrix.Set_In_AV_Out.format(out2[0].strip(), out1[1].strip()))
    return {"Swap": {"Input": out1[0], "Output": out1[1]}, "With": {"Input": out2[0], "Output": out2[1]}}
