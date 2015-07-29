import time, math, mraa, socket, select
from PWMShield import PWMShield

pwmShield = PWMShield(6)

def main():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while(True):    ##Connect to the other edison
        try:
            clientsocket.connect(("172.16.83.218", 8070))
            break
        except socket.error:
            continue

    clientsocket.settimeout(10)
    clientsocket.send('hello')
    print('Connected to Joystick Server')
    socketAlive = True
    while(socketAlive):
        buf = clientsocket.recv(20)
        if(len(buf) > 0): 
            splitBuf = buf.split(',')
            print(splitBuf)
            setDirection(float(splitBuf[0]),float(splitBuf[1]))
        else:
            socketAlive=False

    print('Connection Lost. Shutting down.')
    setDirection(0, 0)
    clientsocket.shutdown(socket.SHUT_RD)
    clientsocket.close()
    exit()

def setDirection(x,y):  
    pwmPins = [0,1,2]
    angles = [90,225,315]
    velocities = []
    scaledVelocities = []

    for i in range(0, 3):   ##Turn the X,Y coordinates of direction into wheel velocities
        velocities.append( (-x*math.sin(math.radians(angles[i]))) + (y*math.cos(math.radians(angles[i]))))

    for i in range(0, 3):   ##Scale the wheel velocities into PWM output period in us
        scaledVelocities.append(velocities[i]*400+1500)

    for i in range(0, 3):   ##Output the pwm pulses on the output pins
        pwmShield.setPulseWidthUs(pwmPins[i],scaledVelocities[i])

main()