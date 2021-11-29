import math


def cosrl(ang, a, b, c):
    if a is None:
        ans = b * math.cos(math.radians(ang)) + math.sqrt((c**2) - (b**2) * (math.sin(math.radians(ang))**2))
    if b is None:
        ans = a * math.cos(math.radians(ang)) + math.sqrt((c**2) - (a**2) * (math.sin(math.radians(ang))**2))
    if c is None:
        ans = math.sqrt((a**2) + (b**2) - 2*a*b*math.cos(math.radians(ang)))
    if ang is None:
        numerator = (a**2) + (b**2) - (c**2)
        denominator = 2*a*b
        ans = math.radians(math.acos(numerator/denominator))
    return ans


print(cosrl(60, 105, 213, None))
