import json
import serial



def read_layout():
    with open("layout.json",'r') as f:
        return json.reads(f.read())

class Game():
    def __init__(self):
        self.serial = serial.Serial('COM3', 9600, timeout=0)
        self.layout = read_layout()

    def send_layout_to_arduino(self):
        layout = read_layout()
        string_to_send = ""
        for line in layout:
            for value in layout:
                string_to_send += str(value)
            string_to_send += '|'

        self.serial.write(string_to_send.encode())

    def send_position_to_arduino(self,position):
        text_to_send = "%d,%d" %position
        self.serial.write(text_to_send.encode())
        