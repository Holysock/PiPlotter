import motorcontrol
import time
import sys 

motor = motorcontrol.MotorControl()
motor.enableMotor(0)

gcode = open(sys.argv[1])
buffer_length = 100
buffer = []

last_t = time.clock()

step_mm = 266.667
feedrate = 350
feedrate_max = 400
pos_x = 0
pos_y = 0
t_per_step = 1/((feedrate*step_mm)/60)

motor.enableMotor(1)

def setFeedrate(feed):
        global t_per_step, feedrate
	feedrate = feed
        t_per_step = 1/((feedrate*step_mm)/60)

def step(x,y,dirx,diry):
	global last_t
	if x or y:
		this_t = time.clock()
		while this_t-last_t < t_per_step:
			this_t = time.clock()

	if x:
		if not (dirx == 0 and not motor.getEnd("x")):
			motor.stepX(dirx)
			global pos_x
			pos_x = pos_x+1 if dirx else pos_x-1

        if y:    
                if not (diry == 0 and not motor.getEnd("y")):
                        motor.stepY(diry)
			global pos_y
                        pos_y = pos_y+1 if diry else pos_y-1
	last_t = time.clock()

def home():
	global feedrate
	tmp = feedrate
	setFeedrate(feedrate_max)
	while motor.getEnd("x") or motor.getEnd("y"):
		step(1,1,0,0)
	global pos_x, pos_y
	pos_x, pos_y = 0, 0
	setFeedrate(tmp)

def step_line(x1, y1):
	x1 = round(x1)
	y1 = round(y1)
	global pos_x, pos_y
	x0 = pos_x
	y0 = pos_y
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	x, y = x0, y0
	sx = -1 if x0 > x1 else 1
	sy = -1 if y0 > y1 else 1
	stpx,stpy,dirx,diry = 0,0,0,0
	if dx > dy:
        	err = dx / 2.0
        	while x != x1:
			stpx,stpy,dirx,diry = 0,0,0,0
            		err -= dy
            		if err < 0:
               			y += sy
				stpy = 1
				diry = 1 if sy > 0 else 0
                		err += dx
      			x += sx
			stpx = 1
			dirx = 1 if sx > 0 else 0
			step(stpx,stpy,dirx,diry)
    	else:
        	err = dy / 2.0
        	while y != y1:
            		stpx,stpy,dirx,diry = 0,0,0,0
            		err -= dx
            		if err < 0:
                		x += sx
                                stpx = 1
                                dirx = 1 if sx > 0 else 0
                		err += dy
            		y += sy
                        stpy = 1
                        diry = 1 if sy > 0 else 0
                        step(stpx,stpy,dirx,diry)        
	step(stpx,stpy,dirx,diry)

def gofast(x1,y1):
	x1 = round(x1)
	y1 = round(y1)
	setFeedrate(feedrate_max)
	dirx = 1 if x1 > pos_x else 0
	diry = 1 if y1 > pos_y else 0
	while pos_x != x1 or  pos_y != y1:
		stpx,stpy = 0,0
		if pos_x != x1:
			stpx = 1
		if pos_y != y1:
			stpy = 1
		step(stpx,stpy,dirx,diry)


def clearbuffer(buf):
	for stuff in buf:
		if stuff[0] == "G1":
			if stuff[4] > 0:
				setFeedrate(stuff[4])
              		if stuff[3] > -1:
                        	motor.setlaser((stuff[3]*100)/255)
			if stuff[1] > -1 and stuff[2] > -1:
				step_line(stuff[1]*step_mm,stuff[2]*step_mm)
		elif stuff[0] == "G0":
			motor.setlaser(0)
			gofast(stuff[1]*step_mm,stuff[2]*step_mm)
		elif stuff[0] == "G28":
			home()

home()
if len(sys.argv) == 5:
	step_line(float(sys.argv[3])*step_mm,float(sys.argv[4])*step_mm)
	pos_x, pos_y = 0, 0

for line in gcode:
	new_command, new_x, new_y, new_z =-1, -1, -1, -1
	new_feedrate = 0
	if 'F' in line:
		fi = line.find("F")
		i = fi+1
		for char in line[fi+1:]:
			if char.isdigit() or char == '.' or char == ',':
				i += 1
			else: break
		if i > fi+1:
			feed = float(line[fi+1:i])
			if feed == 0:
				feed = 0.001
			new_feedrate = feed

	if "G01" in line or "G1" in line:
		xi = line.find("X") 
		yi = line.find("Y")
		zi = line.find("Z")
		if xi == -1 or yi == -1:
			continue
		if zi == -1:
			z = 0
		i = xi+1
		for char in line[xi+1:]:
                        if char.isdigit() or char == '.' or char == ',':
                                i += 1
                        else: break
                if i > xi+1:
                        x = float(line[xi+1:i])
		else: continue

		i = yi+1
		for char in line[yi+1:]:
                        if char.isdigit() or char == '.' or char == ',':
                                i += 1
                        else: break
                if i > yi+1:
                        y = float(line[yi+1:i])
		else: continue

		i = zi+1
		for char in line[zi+1:]:
                        if char.isdigit() or char == '.' or char == ',':
                                i += 1
                        else: break
                if i > zi+1:
                        z = int(line[zi+1:i])
                else: z = 0
		
		new_command = "G1"
		new_x = x
		new_y = y
		new_z = z
		#motor.setlaser((z*100)/255)
		#step_line(step_mm*x,step_mm*y)
		#print(x,y,z)

	elif "G00" in line or "G0" in line:
                xi = line.find("X")
                yi = line.find("Y")
                if xi == -1 or yi == -1:
                        continue
                i = xi+1
                for char in line[xi+1:]:
                        if char.isdigit() or char == '.' or char == ',':
                                i += 1
                        else: break
                if i > xi+1:
                        x = float(line[xi+1:i])
                else: continue

                i = yi+1
                for char in line[yi+1:]:
                        if char.isdigit() or char == '.' or char == ',':
                                i += 1
                        else: break
                if i > yi+1:
                        y = float(line[yi+1:i])
                else: continue
		
		new_command = "G0"
                new_x = x
		new_y = y
                #step_line(step_mm*x,step_mm*y)
                #print(x,y,z)
		
	if not (new_x == -1 and new_y == -1 and new_z == -1 and new_feedrate == -1):
		buffer.append((new_command,new_x,new_y,new_z,new_feedrate))
	
	if len(buffer) >= buffer_length:
		clearbuffer(buffer)
		motor.setlaser(0)
		del(buffer[:])

if len(buffer) > 0:
	clearbuffer(buffer)
        motor.setlaser(0)
        del(buffer[:])

home()
motor.setlaser(0)
motor.enableMotor(0)
motor.off()




