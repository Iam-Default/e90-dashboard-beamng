import socket
import struct
from threading import Thread


class OutgaugeServer(Thread):
    """Outgauge UDP Server thread class"""

    def __init__(self, UDP_IP="", UDP_PORT=4444):
        Thread.__init__(self)
        self.work = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        result = sock.connect_ex(('localhost', 4444))
        if result == 0:
            print("Port is open")
        else:
            print(f"Port 4444 is not open ( {result} )")

        self.sock.bind((UDP_IP, UDP_PORT))
        print(f"Server listening ({UDP_IP}:{UDP_PORT}")
        self.time = 0
        self.car = ""
        self.words = ""
        self.gear = 1
        self.spareb = ""
        self.speed = 0.0  # M/S
        self.RPM = 0.0
        self.turbo = 0.0
        self.engtemp = 0.0
        self.fuel = 0.0
        self.oilpress = 0.0
        # self.spare1=0.0
        # self.spare2=0.0
        # self.spare3=0.0
        self.throttle = 0.0
        self.brake = 0.0
        self.clutch = 0.0
        self.display1 = ""
        self.display2 = ""
        self.dashlights = 0
        self.showlights = 0

    def run(self):
        while self.work:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.time = struct.unpack("I", data[:4])[0]
            self.car = data[4:8]
            self.words = struct.unpack("H", data[8:10])[0]
            self.gear = struct.unpack("H", data[10:12])[0]
            self.spareb = struct.unpack("H", data[12:14])[0]
            self.speed = struct.unpack("f", data[12:16])[0]  # M/S
            self.RPM = struct.unpack("f", data[16:20])[0]
            self.turbo = struct.unpack("f", data[20:24])[0]
            self.engtemp = struct.unpack("f", data[24:28])[0]
            self.fuel = struct.unpack("f", data[28:32])[0]
            self.oilpress = struct.unpack("f", data[32:36])[0]
            self.dashlights = struct.unpack("I", data[44:48])[0]
            self.showlights = struct.unpack("I", data[40:44])[0]
            # self.spare3=struct.unpack("f",data[44:48])[0]
            self.throttle = struct.unpack("f", data[48:52])[0]
            self.brake = struct.unpack("f", data[52:56])[0]
            self.clutch = struct.unpack("f", data[56:60])[0]
            self.display1 = data[60:76]
            self.display2 = data[76:92]
            #outgauge_pack = struct.unpack('I3sxH2B7f2I3f15sx15sxI', data)
            # print "ID :", struct.unpack("i",data[92:96])
