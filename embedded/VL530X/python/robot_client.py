# Verbose debugging if arg -v
if len(sys.argv) == 2 and sys.argv[2].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)


# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 5
sensor2_shutdown = 6
sensor3_shutdown = 13
sensor4_shutdown = 19
GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)
GPIO.setup(sensor3_shutdown, GPIO.OUT)
GPIO.setup(sensor4_shutdown, GPIO.OUT)


# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)
GPIO.output(sensor3_shutdown, GPIO.LOW)
GPIO.output(sensor4_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.5)

# Create one object per VL53L0X passing the address to give to
# each.
tof1 = VL53L0X.VL53L0X(address=0x3B)
tof2 = VL53L0X.VL53L0X(address=0x3D)
tof3 = VL53L0X.VL53L0X(address=0x3F)
tof4 = VL53L0X.VL53L0X(address=0x4B)

# Set shutdown pin high for the first VL53L0X then
# call to start ranging
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.5)
tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then
# call to start ranging
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

GPIO.output(sensor3_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof3.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

GPIO.output(sensor4_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof4.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof1.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

# Init socket


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('attempting connect\n')
clientsocket.connect(('130.229.142.225', int(sys.argv[1])))
print('Connection open\n')
clientsocket.send('Connection open\n')
time.sleep(1)
print('Start sending data\n')
clientsocket.send('Start sending position update\n')
id = "BOT1"
packetno = 0

print('Reading sensor data, press Ctrl-C to quit...')


def ranging(threadname, q):
	while (True):

		global tof
		print("Getting distance values")
		tof_Front = tof1.get_distance()
		time.sleep(0.02)
		tof_Left = tof2.get_distance()
		time.sleep(0.02)
		tof_Right= tof3.get_distance()
		time.sleep(0.02)
		tof_Back = tof4.get_distance()
		time.sleep(0.02)
		#print ("Front: %f, Left: %f, Right: %f, Back: %f" (tof_Front, tof_Left, tof_Right, tof_Back))
		tof = (str(tof_Front) + "#" + str(tof_Back) + "#" + str(tof_Left) + "#" + str(tof_Right) + "#")
		time.sleep(0.02)

def client(threadname, q, steps):
	while(True):
		print("client initiated")
		global tof
		global stepno
		msg=str(id) + "#" + "FWD" + "#" + str(stepno) + "#" +  str(tof) + "$"
		print(msg)
		clientsocket.send(msg)
		time.sleep(0.1)

def Main():

	global tof
	M=MOTOR()
	t1 = threading.Thread(target=ranging, args=("TOF", tof))
	t2 = threading.Thread(target=client, args=("Client", tof, stepno))
	#t3 = threading.Thread(target=motor_move, args=())
	t1.start()
	t2.start()

	While (1):
			DISTANCE = raw_input("Distance [mm]:")
			M.motor_move(FW,float(DISTANCE), 1.0/1500.0)
#t3.start()
#	t1.join()
#	t2.join()
	#t3.join()


if __name__ == '__main__':
	Main()
#tof1.stop_ranging()
#GPIO.output(sensor1_shutdown, GPIO.LOW)
#tof2.stop_ranging()
#GPIO.output(sensor2_shutdown, GPIO.LOW)
#tof3.stop_ranging()
#GPIO.output(sensor3_shutdown, GPIO.LOW)
#tof4.stop_ranging()
#GPIO.output(sensor4_shutdown, GPIO.LOW)
