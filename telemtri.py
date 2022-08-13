import json
from datetime import datetime
import socket
import time

from dronekit import Command, connect, VehicleMode, LocationGlobalRelative, CommandSequence
mikrosaniye =0
milisaniye =0


s = socket.socket()
# Bağlanılacak adres ve port
host = "127.0.0.1"
port = 25002

#vehicle = connect('com5',baud=57600)
#vehicle = connect('com5',baud=57602)
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True )

def listen_SYSTEM_TIME(vehicle):
    @vehicle.on_message("SYSTEM_TIME")
    def listener(self, name, msg):
        global mikrosaniye
        #global milisaniye

       # milisaniye = msg.time_boot_ms
        mikrosaniye = msg.time_unix_usec
        #print(msg)

    return mikrosaniye




    #mlsec = unix_time.split('.')[1][:3]

"""
MANUAL
STABILIZE




AUTO
GUIDED
CIRCLE
RTL

"""

otonomdurumu = 0

def veri():
    unix_time = listen_SYSTEM_TIME(vehicle)
    unix_time = (float)(unix_time / 1000000)
    gps = "{ \"saat\": "+datetime.utcfromtimestamp(unix_time).strftime('%H')+", \"dakika\": "+datetime.utcfromtimestamp(unix_time).strftime('%M')+", \"saniye\": "+datetime.utcfromtimestamp(unix_time).strftime('%S')+", \"milisaniye\": "+datetime.utcfromtimestamp(unix_time).strftime('%f')+"}"
    if vehicle.mode.name == "MANUAL" or vehicle.mode.name == "STABILIZE":
        otonomdurumu = 0
    else:
        otonomdurumu = 1

    data = {
        "takim_numarasi": 0,
        "IHA_enlem": vehicle.location.global_relative_frame.lat,
        "IHA_boylam": vehicle.location.global_relative_frame.lon,
        "IHA_irtifa": vehicle.location.global_relative_frame.alt,
        "IHA_dikilme": vehicle.attitude.pitch,
        "IHA_yatis": vehicle.attitude.roll,
        "IHA_yonelme": vehicle.attitude.yaw,
        "IHA_hiz": vehicle.groundspeed,
        "IHA_batarya": vehicle.battery.voltage,
        "IHA_otonom": otonomdurumu,
        "IHA_kilitlenme": 0,
        "Hedef_merkez_X": 0,
        "Hedef_merkez_Y": 0,
        "Hedef_genislik": 0,
        "Hedef_yukseklik": 0,
        "GPSSaati": gps,
    }

    return json.dumps(data)

try:
    # Bağlantıyı yap
    s.connect((host, port))
    print("Bağlantı yapıldı")
    # serverden yanıtı al

except socket.error as msg:
    print("[Server aktif değil.] Mesaj:", msg)

posString = "baglanti_kuruldu_telemetri"
s.sendall(posString.encode("UTF-8"))

while True:
    posString = "bağlantı dinleniyor1"
    receivedData = s.recv(1024).decode("UTF-8")  # receiveing data in Byte fron C#, and converting it to String
    posString = "bağlantı dinleniyor"
    if  (receivedData == "telemetri"  ):
        time.sleep(0.2)
        data = veri()
        # data = "merhaba"
        print(data)
        print("\n")

        if data is not None:
            s.sendall(data.encode('utf-8'))
        else:
            s.sendall(data)

    elif receivedData == "bos":
        posString4 = "bosDegeriAldım"
        s.sendall(posString4.encode('utf-8'))



