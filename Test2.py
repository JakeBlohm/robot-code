from ArmPositioner import END_EFFECTOR_OFFSET
from localMath import *

x= 0
y= 0
z = 0

while True:
	endEffectorone = int(input())
	endEffectortwo = int(input())
	Temp = (END_EFFECTOR_OFFSET * math.cos(math.radians(endEffectortwo)))
	if endEffectorone < 0:
		Temp = Temp
	x = 10 - (soh(endEffectorone, None, Temp))
	y = 10 - (cah(endEffectorone, None, Temp))
	z = 10 - (END_EFFECTOR_OFFSET * math.sin(math.radians(endEffectortwo)))
	xO, yO, zO = 10 - x, 10 - y, 10 - z
	xz = pT(x,z)
	try:
		print(soh(None,xz,END_EFFECTOR_OFFSET))
	except:
		print("ERROR")
	try:
		print(toa(None,xz,y))
	except:
		print("ERROR")
	try:
		print(cah(None,y,END_EFFECTOR_OFFSET))
	except:
		print("ERROR")