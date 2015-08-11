import time, math, mraa
from PWMShield import PWMShield

pwmShield = PWMShield(6)
def main():
    enabled = True

    print("Ready to go!")
    while(enabled):
        input = raw_input('')
        if(input == 'w'):        #If input is w arrow key
            setDirection(0,.5)   #Tell robot to move forward

        if(input == 'a'):        ##If input is a arrow key
            setDirection(-.5,0)   ##Tell robot to move left

        if(input == 's'):        ##If input is s arrow key
            setDirection(0,-.5)   ##Tell robot to move backward

        if(input == 'd'):        ##If input is W arrow key
            setDirection(.5,0)   ##Tell robot to move right
        if(input == ' 'or input == ''):        ##If input is spacebar
            setDirection(0,0)   ##Stop the robot

def setDirection(x,y):
    pwmPins = [0,1,2]
    angles = [90,210,330]
    velocities = []
    scaledVelocities = []

    for i in range(0, 3):   ##Turn the X,Y coordinates of direction into wheel velocities
		velocities.append( (-x*math.sin(math.radians(angles[i]))) + (y*math.cos(math.radians(angles[i]))))
    print( str(velocities))

    for i in range(0, 3):   ##Scale the wheel velocities into PWM output period in us
		scaledVelocities.append(velocities[i]*400+1500)
    print(str(scaledVelocities))
    for i in range(0, 3):   ##Output the pwm pulses on the output pins
        pwmShield.setPulseWidthUs(pwmPins[i],scaledVelocities[i])

main()
