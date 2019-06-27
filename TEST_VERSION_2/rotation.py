import math
def rotation(a,b):
    ax, ay = a
    bx, by = b
    angle = math.degrees(math.atan2(by-ay,bx-ax)) + 90
    return angle
