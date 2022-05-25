import csv
import random
import sys

devices = 0
counter = 1
header = ['No', ' ', 'bandwidth (MB)']
bandwidth = [10, 20, 50, 100, 200, 300, 500, 1000]

def randomBandwidth():
    return bandwidth[random.randrange(0, len(bandwidth), 1)]

# check for extra vars
if len(sys.argv) > 1:
    devices = int(sys.argv[0])
else:
    devices = 502

# open the file ( with keyword means you don't have to close)
with open('config.csv', 'w', encoding='UTF8', newline='') as f:

    # Create the writer 
    writer = csv.writer(f)

    # Write the header
    writer.writerow(header)

    while(counter != devices):
        data = [counter, '', randomBandwidth()]
        writer.writerow(data)
        counter += 1



