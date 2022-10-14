import math
import numpy as np

def quadratic_discriminant(a,b,c) -> float:
    d = b**2 - 4*a*c
    return d

def quadratic(a,b,c) -> tuple(float,float): # Basic quadratic equation using math, returns a tuple
    discriminant = math.sqrt(b**2 - 4 * a *c)
    denominator = 2*a
    x1 = (-b + discriminant)/denominator
    x2 = (-b - discriminant)/denominator
    return (x1, x2)

def loh_quadratic(b,c) -> tuple(float,float): # WHERE a = 1!! Professor Po-Shen Loh's quadratic equation using math, returns a tuple
    midpoint = -b * 0.5
    u = math.sqrt(-c+midpoint**2)
    x1 = midpoint + u
    x2 = midpoint - u
    return (x1, x2)
   
def soh(o=None,h=None,theta=None) -> float: # theta is always in radians
    if o is None:
        return math.sin(theta) * h
    elif h is None:
        return o / math.sin(theta)
    elif theta is None:
        return math.asin(o/h)

def cah(a=None,h=None,theta=None) -> float: # theta is always in radians
    if a is None:
        return math.cos(theta) * h
    elif h is None:
        return a / math.cos(theta)
    elif theta is None:
        return math.acos(a/h)

def toa(o=None,a=None,theta=None) -> float: # theta is always in radians
    if o is None:
        return math.tan(theta) * a
    elif a is None:
        return o / math.tan(theta)
    elif theta is None:
        return math.atan(o/a)

def cos_rule(a=None,b=None,c=None,gamma=None) -> float: # gamma always in radians
    if a is None:
        return b * math.cos(gamma) + math.sqrt(c**2 - b**2 * (math.sin(gamma)**2))
    elif b is None:
        return a * math.cos(gamma) + math.sqrt(c**2 - a**2 * (math.sin(gamma)**2))
    elif c is None:
        return math.sqrt(a**2+b**2-2*a*b*math.cos(gamma))
    elif gamma is None:
        numerator = a**2+b**2-c**2
        denominator = 2*a*b
        return math.acos(numerator/denominator)

def pythagoras(a=None,b=None,c=None) -> float: # Basic pythagoras
    if a is None:
        return c**2 - b**2
    elif b is None:
        return c**2 - a**2
    elif c is None:
        return a**2 + b**2