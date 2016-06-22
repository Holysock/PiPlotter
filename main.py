import motorcontrol
import time
import sys 

motor = motorcontrol.MotorControl()
motor.enableMotor(0)

gcode = open(sys.argv[1])

step_mm = 266,667
feedrate = 0.0

for line in gcode:
	if 'F' in line:
		line = line[1:]
		i = 0
		for char in line:
			if char.isdigit() or char == '.' or char == ',':
				i += 1
			else:
				 break
def line():
	pass


