import math

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier

a = 1.4
b = 1.5
c = 2.4
d = 2.5
print(round(a), round(b), round(c), round(d))
print(round_half_up(a), round_half_up(b), round_half_up(c), round_half_up(d))