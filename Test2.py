import math

def aTan(X,Y,mode):
	if Y != 0:
		if X == 0 and Y < 0:
			m = 180
		elif X== 0 and Y > 0:
			m = 0
		else:
			if mode == 1:
				m  = (math.degrees(math.atan(X/Y)))
			if mode == 2:
				m = (math.degrees(math.asin(X/Y)))
		if Y < 0 and X > 0:
			m += 180
		elif Y < 0 and X < 0:
    			m -= 180
	elif X < 0:
		m = -90
	elif X > 0:
		m = 90
	else:
		m = 0
	return m

#print(math.degrees(math.atan(1/0)))
print(aTan(0,1,1))
#print(math.degrees(math.asin(1/0)))
print(aTan(1,0,2))