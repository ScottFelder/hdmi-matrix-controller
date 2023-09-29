import socket
from enum import Enum


class Power(Enum):
    OFF = "off"
    ON = "on"


class HdmiMatrix:
    # Power  Command Codes
    Read_Power = "r power!"
    Set_Power = "s power {0}!"
    Set_Reboot = "s reboot!"

    # System Setup Command Codes
    Read_Status = "r status!"
    Read_Firmware = "r fw version!"
    Read_Link_In = "r link in {0}!"
    Read_Link_Out = "r link out {0}!"
    Set_Reset = "s reset!"
    Set_Beep = "s beep {0}!"
    Read_Beep = "r beep!"
    Set_Lock = "s lock {0}!"
    Read_Lock = "r lock!"
    Set_LCD_On_Time = "s lcd on time {0}!"
    Read_LCD_Model = "r lcd model!"
    Set_Save_Preset = "s save preset {0}!"
    Set_Recall_Preset = "s recall preset {0}!"
    Set_Clear_Preset = "s clear preset {0}!"
    Read_Preset = "r preset {0}!"

    # Output Setting Command Codes
    Set_In_AV_Out = "s in {0} av out {1}!"
    Read_AV_Out = "r av out {0}!"
    Set_HDMI_Stream = "s hdmi {0} stream {1}!"
    Read_HDMI_Stream = "r hdmi {0} stream!"
    Set_HDMI_Scaler = "s hdmi {0} scaler {1}!"
    Read_HDMI_Scaler = "r hdmi {0} scaler!"

    # EDID Setting Command Codes
    Set_EDID_In_From = "s edid in {0} from {1}!"
    Read_EDID_In = "r edid in {0}!"
    Read_EDID_Data_HDMI = "r edid data hdmi {0}!"

    # CEC Setting Command Codes
    Set_CEC_In_On = "s cec in {0} on!"
    Set_CEC_In_Off = "s cec in {0} off!"

    # Network Setting Command Codes
    Read_IpConfig = "r ipconfig!"

    def __init__(self, i, o, s):
        self.inputs = i
        self.outputs = o
        self.socket = s

    def exec_command(self, cmd):
        print(cmd)
        self.socket.send(cmd.encode())
        ret = self.socket.recv(51200).decode()
        print(ret)
        return ret
