from math import cos, radians, sin
import random

angle = random.randint(0,180)
radius = 1920 / 2

x = radius * sin(radians(angle))
y = radius * cos(radians(angle))

print(f'point is: {x, y} at an angle: {angle}')