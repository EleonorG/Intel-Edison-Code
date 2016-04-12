import mraa

def getDistance():
	pin = mraa.Aio(0)
	value = pin.read()
	voltage = value*(5/1024.0)
	distance = .171+12.4/voltage
	return distance