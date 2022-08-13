from dronekit import Command, connect, VehicleMode, LocationGlobalRelative, CommandSequence
vehicle = connect('com5', wait_ready=True , baud=57600)

def veri():
    data = {
        "takim_numarasi": 1,
        "IHA_enlem": vehicle.location.global_relative_frame.lat,
        "IHA_boylam": vehicle.location.global_relative_frame.lon,
        "IHA_irtifa": vehicle.location.global_relative_frame.alt,
        "IHA_dikilme": 5,
        "IHA_yonelme": vehicle.heading,
        "IHA_yatis": 0,
        "IHA_hiz": vehicle.groundspeed,
        "IHA_batarya": vehicle.battery,
        "IHA_otonom": vehicle.mode.name,

    }
    return data
while True:
    print(veri())