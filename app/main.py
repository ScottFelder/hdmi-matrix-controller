from fastapi import FastAPI
from .hdmi_matrix import HdmiMatrix, Power
import socket
import os

app = FastAPI()

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
