from dorna import Dorna
import json
import time
import sys
import signal
import os

robot = None
rest_joint = [0,110,-90,30,-90]

def try_connect():
	global robot

	robot = Dorna()
	result = json.loads(robot.connect(port_name='/dev/cu.usbmodem1424401'))
	if (result["connection"] == 2) :
		print("Connected successfully to robot at port \"" + result["port"] + "\"")
		return True
	else:
		return False

def try_shutdown():
	global robot

	if (json.loads(robot.device())["connection"]!=0):
		print("Shutting down the robot... ",end="")
		robot.terminate()
		print("complete.")

def home():

	# home all joints
	robot.home(["j0", "j1", "j2", "j3"])
	print("All joints have been homed.")

	# Move to a known position
	result = robot.play({"command": "move", "prm":{"path": "joint", "movement":0, "joint":rest_joint}})
	result = json.loads(result)
	wait = robot._wait_for_command(result, time.time()+1000)
	print("Robot is ready to receive commands.")

def main():

	# Try to connect to the robot
	nAttempts = 5
	while (nAttempts >= 0):
		if try_connect():
			break
		else:
			nAttempts -= nAttempts
			time.sleep(3)
	if (nAttempts < 0):
		return 0

	# Home the robot
	home();

	while(True):
		time.sleep(1)

	return 1

if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		try_shutdown()
		try:
			sys.exit(0)
		except:
			os._exit(0)
