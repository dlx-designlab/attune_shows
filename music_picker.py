# No. of Apex / Density > Instrument (4)
# Position / Distribution > Octaves (4)
# Brightness > Scale of Sound (4)
import math
from itertools import combinations
import csv
from icecream import ic

# Each line in the csv file contains the coordinates of the detected apex points an image.
# Thre is an even number of coordinates per line. each pair is X and Y. 
# for example [0] is X and [1] is Y. [2] is X and [3] is Y....
uuid = "FCB89A"
csv_file = f"app/static/caps_img/{uuid}/{uuid}.csv"
txt_file = f"app/static/caps_img/{uuid}/{uuid}.txt"
data = []

def dist(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def remap_values(value, fromMin, fromMax, toMin = 0, toMax = 3):
    # Figure out how 'wide' each range is
    fromRange = fromMax - fromMin
    toRange = toMax - toMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - fromMin) / float(fromRange)

    # Convert the 0-1 range into a value in the right range.
    return toMin + (valueScaled * toRange)


# load CSV file
with open(csv_file, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        data.append(row)
        
# Calculate capillary density, distribution, and brightness
cap_density = 0         # average ammount of apex points in a sample
cap_distribution = 0    # average distance between apex points in a sample
cap_brightness = 0      # average brightness of the sample


# convert data to coordinates
clean_data = []
for item in data:
    # convert csv data to coordinates (x, y) format
    coordinates_data = []
    for i in range(0, len(item), 2):
        coordinates_data.append( (int(item[i]), int(item[i+1])) )
    
    # count the ammount of apex points in the sample
    cap_density += len(coordinates_data)

    # calculate average distance between apex points
    distances = [dist(p1, p2) for p1, p2 in combinations(coordinates_data, 2)]
    avg_distance = sum(distances) / len(distances)
    cap_distribution += avg_distance

    # add coordinates to the clean data list
    clean_data.append(coordinates_data)


cap_density = int(cap_density / len(clean_data))
cap_distribution = int(cap_distribution / len(clean_data))
cap_brightness = 0

ic(cap_density)
ic(cap_distribution)
ic(cap_brightness)

# remap values to a range of 0-3 and struct a filename to match the music file names
# Todo: find correct ranges for cap_density, cap_distribution, cap_brightness
values_filename = f"{int(remap_values(cap_density, 0, 30,))}{int(remap_values(cap_distribution, 100, 1000,))}{int(cap_brightness)}"
print(values_filename)

with open(txt_file, 'w') as txtfile:
    txtfile.write(values_filename)
