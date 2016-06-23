import RPi.GPIO as GPIO

class MotorControl:
	enable = 8
	step_X = 16
	step_Y = 10
	dir_X = 18
	dir_Y = 12 
	end_X = 32
	end_Y = 36
	laser = 29

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(enable,GPIO.OUT)
	GPIO.setup(step_X,GPIO.OUT)
	GPIO.setup(step_Y,GPIO.OUT)
	GPIO.setup(dir_X,GPIO.OUT)
        GPIO.setup(dir_Y,GPIO.OUT)
	GPIO.setup(laser,GPIO.OUT)
	GPIO.setup(end_X, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(end_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	l = GPIO.PWM(laser,100)
	l.start(0)

	def enableMotor(self,b):
		if b:
			GPIO.output(self.enable, False)
		else:
			GPIO.output(self.enable, True)
	
	def stepX(self,dir):
		GPIO.output(self.dir_X,dir)
		GPIO.output(self.step_X,True)
		GPIO.output(self.step_X,False)

	def stepY(self,dir):
                GPIO.output(self.dir_Y,dir)
                GPIO.output(self.step_Y,True)
                GPIO.output(self.step_Y,False)
	
	def getEnd(self,a):
		if a == "x":
			return GPIO.input(self.end_X)
		elif a == "y":
			return GPIO.input(self.end_Y)
	
	def setlaser(self,pwm):
		self.l.ChangeDutyCycle(pwm)

	def off(self):
		GPIO.output(self.enable, True)
		l.stop()
		#GPIO.cleanup()
