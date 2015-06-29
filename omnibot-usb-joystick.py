from evdev import InputDevice, categorize, ecodes, list_devices
from PWMShield import PWMShield

pwmShield = PWMShield(6)

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
			if(event.code ==1):
				y_scaled = event.value-512.0
				y_scaled = -y_scaled/512
				setDirection(x_scaled,y_scaled)

def selectDevice():
	'''Select a device from the list of accessible input devices.'''
	devices = [InputDevice(i) for i in reversed(list_devices('/dev/input/'))]
	if(len(devices) > 2):
		return devices[2]
	else:
		print("No joysticks found!")
		exit()

def setDirection(x,y):
    pwmPins = [0,1,2]
    angles = [90,225,315]
    velocities = []
    scaledVelocities = []

    for i in range(0, 3):   ##Turn the X,Y coordinates of direction into wheel velocities
        velocities.append( (-x*math.sin(math.radians(angles[i]))) + (y*math.cos(math.radians(angles[i]))))
    print( str(velocities))

    for i in range(0, 3):   ##Scale the wheel velocities into PWM output period in us
        scaledVelocities.append(velocities[i]*500+1500)

    for i in range(0, 3):   ##Output the pwm pulses on the output pins
        pwmShield.setPulseWidthUs(pwmPins[i],scaledVelocities[i])

main()