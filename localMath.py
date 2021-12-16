import math


def pT(a, b, c=0):
    return math.sqrt(a ** 2 + b ** 2 + c ** 2)


def soh(ang, opp, hyp):
    if opp is None:
        ans = hyp * math.sin(math.radians(ang))
    elif hyp is None:
        ans = opp / math.sin(math.radians(ang))
    elif ang is None:
        ans = math.degrees(math.asin(opp / hyp))
    else:
        print("Could not find missing data")
    return ans


def cah(ang, adj, hyp):
    if adj is None:
        ans = hyp * math.cos(math.radians(ang))
    elif hyp is None:
        ans = adj / math.cos(math.radians(ang))
    elif ang is None:
        ans = math.degrees(math.acos(adj / hyp))
    else:
        print("Could not find missing data")
    return ans


def toa(ang, opp, adj):
    if opp is None:
        ans = adj * math.tan(math.radians(ang))
    elif adj is None:
        ans = opp / math.tan(math.radians(ang))
    elif ang is None:
        if adj != 0:
            ans = math.degrees(math.atan(opp / adj))
        else:
            ans = 90
    else:
        print("Could not find missing data")
    return ans


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
        ans = math.degrees(math.acos(numerator/denominator))
    return ans
