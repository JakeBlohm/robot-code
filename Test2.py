from ArmPositioner import END_EFFECTOR_OFFSET
from localMath import *

X= 0
Y= 0
Z = 0

while True:
	endEffectorone = int(input())
	endEffectortwo = int(input())
	Temp = (END_EFFECTOR_OFFSET * math.cos(math.radians(endEffectortwo)))
	if endEffectorone < 0:
		Temp = -Temp
	x = (soh(endEffectorone, None, Temp))
	y = (cah(endEffectorone, None, Temp))
	z = (soh(endEffectortwo, None, END_EFFECTOR_OFFSET))
	xz = pT(x,z)
	print("{} <----This is 10 right?".format(pT(x,y,z)))
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