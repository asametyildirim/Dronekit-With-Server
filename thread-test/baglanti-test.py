import threading
import time
import json
from datetime import datetime
import socket
from dronekit import Command, connect, VehicleMode, LocationGlobalRelative, CommandSequence

vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True )
# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
mikrosaniye = 0

def print_cube(vehicle):
      # function to print cube of given num
      while True:
       print(vehicle.location.global_relative_frame.lat)


def telemetri(vehicle):
      # vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True )
      otonomdurumu = 0

      def listen_SYSTEM_TIME(vehicle):
         @vehicle.on_message("SYSTEM_TIME")
         def listener(self, name, msg):
            global mikrosaniye
            # global milisaniye

            # milisaniye = msg.time_boot_ms
            mikrosaniye = msg.time_unix_usec
            #print(mikrosaniye)
            # print(msg)

         return mikrosaniye

         # mlsec = unix_time.split('.')[1][:3]


      otonomdurumu = 0
      def veri():
         unix_time = mikrosaniye
         print(mikrosaniye)
         print(unix_time)
         unix_time = (float)(unix_time / 1000000)
         gps = "{ \"saat\": " + datetime.utcfromtimestamp(unix_time).strftime(
            '%H') + ", \"dakika\": " + datetime.utcfromtimestamp(unix_time).strftime(
            '%M') + ", \"saniye\": " + datetime.utcfromtimestamp(unix_time).strftime(
            '%S') + ", \"milisaniye\": " + datetime.utcfromtimestamp(unix_time).strftime('%f') + "}"
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

      while True:
         listen_SYSTEM_TIME(vehicle)
         time.sleep(1)
         data = veri()
         print(data)
         print("\n")


if __name__ == "__main__":
   # creating thread
   t1 = threading.Thread(target=telemetri, args=(vehicle,))
   #t2 = threading.Thread(target=print_cube, args=(vehicle,))
   #t2.start()
   # starting thread 1
   t1.start()
   # starting thread 2


   # wait until thread 1 is completely executed

   # wait until thread 2 is completely executed


   # both threads completely executed
   print("Done!")