from datetime import datetime
import socket
import time

from dronekit import Command, connect, VehicleMode, LocationGlobalRelative, CommandSequence
mikrosaniye =0
milisaniye =0


#vehicle = connect('com5',baud=57602)
#vehicle = connect('com5',baud=57600)


vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True )
otonomdurumu = 0
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
        "iha_enlem": vehicle.location.global_relative_frame.lat,
        "iha_boylam": vehicle.location.global_relative_frame.lon,
        "iha_irtifa": vehicle.location.global_relative_frame.alt,
        "iha_dikilme": vehicle.attitude.pitch,
        "IHA_yatis": vehicle.attitude.roll,
        "iha_yonelme": vehicle.attitude.yaw,
        "iha_hiz": vehicle.groundspeed,
        "iha_batarya": vehicle.battery.voltage,
        "iha_otonom": otonomdurumu,
        "iha_kilitlenme": 0,
        "Hedef_merkez_X": 315,
        "Hedef_merkez_Y": 220,
        "Hedef_genislik": 12,
        "Hedef_yukseklik": 46,
        "GPSSaati" : gps,

    }
    return data

while True:
    time.sleep(1)
    data = veri()
    print(data)
    print("\n")


