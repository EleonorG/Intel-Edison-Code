from evdev import InputDevice, categorize, list_devices, ecodes

def main():
	x_scaled = 0.0
	y_scaled = 0.0

	joystick = selectDevice()
	print("Joystick Initialized\n")
	for event in joystick.read_loop():
		if event.type == ecodes.EV_ABS:
			if(event.code == 0):
				x_scaled = event.value-512.0
				x_scaled = x_scaled/512
				printPosition(x_scaled,y_scaled)
			if(event.code ==1):
				y_scaled = event.value-512.0
				y_scaled = -y_scaled/512
				printPosition(x_scaled,y_scaled)

def selectDevice():
    '''Connect to the joystick or quit if one is not connected'''
    devices = [InputDevice(i) for i in reversed(list_devices('/dev/input/'))]
    if(len(devices) > 2):
        return devices[2]
    else:
        print("No joysticks found!)")
        exit()

def printPosition(x,y):
	print("Position: {0}, {1}".format(x,y))

main()