import numpy as np
from time import sleep
import RPi.GPIO as GPIO


M2 = 18
M1 = 15
M0 = 14

DIR1 = 20   #Direction GPIO Pin
DIR2 = 16

STEP = 21  # Step GPIO Pin
SLEEP = 27

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
FW = 1
BW = 0

def motor_setup():

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DIR1, GPIO.OUT)
	GPIO.setup(DIR2, GPIO.OUT)
	GPIO.setup(STEP, GPIO.OUT)
	GPIO.output(DIR1, CCW)
	GPIO.output(DIR2, CCW)
	GPIO.setup(M2, GPIO.OUT)
	GPIO.setup(M2, GPIO.OUT)
	GPIO.setup(M1, GPIO.OUT)
	GPIO.setup(M0, GPIO.OUT)
	GPIO.setup(SLEEP, GPIO.OUT)
	GPIO.output(SLEEP, 0)

	GPIO.output(M2,0)
	GPIO.output(M1,0)
	GPIO.output(M0,0)

	VELMAX=1.0/1664

def motor_turn(rotation_direction, rotation_degree, max_velocity, tilt_ramp=10.0):

        stepspermm = 2048.0/(75.61*np.pi)
        stepperdegree = ((215.0*np.pi)/360)*stepspermm

        STEPCOUNTf = stepperdegree*rotation_degree   # Steps per Revolution (360 / 7.5)
        STEPCOUNT = int(STEPCOUNTf) 	#Whole steps

        STARTDELAY =100 		#Denominator  of delay  fraction  
        NBRSTEP =0			#How many steps has happened
        RAMP = STEPCOUNT/2
        print(STEPCOUNT)
	GPIO.output(SLEEP, 1)
        GPIO.output(DIR1, rotation_direction)
        GPIO.output(DIR2, rotation_direction)

        for x in range(STEPCOUNT):
                if NBRSTEP < RAMP:	#Positive acceleration
                   STARTDELAY +=1*tilt_ramp
                   delay = 1.0/STARTDELAY

                if NBRSTEP > RAMP:	#Negative acceleration
                    STARTDELAY -=1*tilt_ramp
                    delay = 1.0/STARTDELAY

                if delay<max_velocity:	#Continiuous speed
                   delay = max_velocity

                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)

                NBRSTEP+=1
		

	GPIO.output(SLEEP, 0)

def motor_move(movement_direction,movement_distance, max_velocity, tilt_ramp=10.0):
	
	global stepno
        stepspermm = 2048.0/(75.61*np.pi)

        STEPCOUNTf = stepspermm*movement_distance   # Steps per Revolution (360 / 7.5)
        STEPCOUNT = int(STEPCOUNTf)     #Whole steps

        STARTDELAY =100                 #Denominator  of delay  fraction  
        NBRSTEP =0                      #How many steps has happened
        RAMP = STEPCOUNT/2
        print(STEPCOUNT)
        GPIO.output(SLEEP, 1)
	if movement_direction:
       		 GPIO.output(DIR1, CW)
        	 GPIO.output(DIR2, CCW)

	else:
		GPIO.output(DIR1, CCW)
                GPIO.output(DIR2, CW)

        for x in range(STEPCOUNT):
                if NBRSTEP < RAMP:      #Positive acceleration
                   STARTDELAY +=1*tilt_ramp
                   delay = 1.0/STARTDELAY

                if NBRSTEP > RAMP:      #Negative acceleration
                    STARTDELAY -=1*tilt_ramp
                    delay = 1.0/STARTDELAY

                if delay<max_velocity:  #Continiuous speed
                   delay = max_velocity

                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
	        sleep(delay)

                NBRSTEP+=1
		stepno=NBRSTEP
		print(stepno)

        GPIO.output(SLEEP, 0)





#motor_turn(CW,180,VELMAX)  	#Turn clockwise, 180 degrees with lowest delay of VELMAX)

#motor_move(FW,100.0, VELMAX)
#sleep(5)
#motor_move(BW,100.0, VELMAX)
#motor_turn(CCW,180,VELMAX)
#sleep(1)

#GPIO.cleanup()

