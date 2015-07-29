from evdev import InputDevice, categorize, ecodes, list_devices
import time, socket

def sendPacket(x,y,connection):
	packet = '{:+f}, {:+f}'.format(x, y)
	print("PACKET:" +packet)
	try:
		connection.send(packet)
	except IOError as e:
		if e.errno == errno.EPIPE:
			print("Connection Lost. Shutting down.")
			exit()
		else:
			print("Exception occured while sending packet.")


def selectDevice():
	'''Connect to the joystick or quit if one is not connected'''
	devices = [InputDevice(i) for i in reversed(list_devices('/dev/input/'))]
	if(len(devices) >2):
		return devices[2]
	else:
		print("No joysticks found!)")
		exit()

def main():
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind(('', 8070))
	serversocket.listen(5) # become a server socket, maximum 5 connections
	print('Server started')

	connection, address = serversocket.accept()
	print("Connection accepted")
	buf = connection.recv(64)

	x_scaled = 0.0
	y_scaled = 0.0

	dev = selectDevice()

	print("Joystick Initialized\n")
	for event in dev.read_loop():
		if event.type == ecodes.EV_ABS:
			if(event.code == 0):
				x_scaled = event.value-512.0
				x_scaled = x_scaled/512
			if(event.code ==1):
				y_scaled = event.value-512.0
				y_scaled = -y_scaled/512
				sendPacket(x_scaled,y_scaled, connection)
	connection.close()
	exit()

main()