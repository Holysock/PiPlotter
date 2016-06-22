import time
import RPi.GPIO as GPIO
import sys

enable = 8
stepX = 16
stepY = 10
dirX = 18
dirY = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(enable,GPIO.OUT)
GPIO.setup(stepX,GPIO.OUT)
GPIO.setup(stepY,GPIO.OUT)
GPIO.setup(dirX,GPIO.OUT)
GPIO.setup(dirY,GPIO.OUT)

GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(enable,True)

GPIO.output(dirX, int(sys.argv[1]))
GPIO.output(dirY, int(sys.argv[2]))

b = False
GPIO.output(enable,False)
#GPIO.output(stepY,True)

while 1:
	if b == True:
		b = False
		#if GPIO.input(36):
		GPIO.output(stepY,True)
		#if GPIO.input(32):
		GPIO.output(stepX,True)
	elif b == False :
		b = True
		GPIO.output(stepY,False)
		GPIO.output(stepX,False)
		time.sleep(0.0004)

