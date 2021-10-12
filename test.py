import math
from itertools import combinations
from icecream import ic

def dist(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

x = [89.86, 23.0, 9.29, 55.47, 4.5, 59.0, 1.65, 56.2, 18.53, 40.0]
y = [78.65, 28.0, 63.43, 66.47, 68.0, 69.5, 86.26, 84.2, 88.0, 111.0]

points = list(zip(x,y))
distances = [dist(p1, p2) for p1, p2 in combinations(points, 2)]
avg_distance = sum(distances) / len(distances)

ic(points)
ic(distances)
ic(avg_distance)