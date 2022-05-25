import csv
import random
import sys

devices = 502
counter = 1
header = ['No', ' ', 'bandwidth (MB)']
bandwidth = [10, 20, 50, 100, 200, 300, 500, 1000]

def randomBandwidth():
    return bandwidth[random.randrange(0, len(bandwidth), 1)]

def generateCSV():
# check for extra vars
    if len(sys.argv) > 1:
        devices = sys.argv[0]

        # open the file ( with keyword means you don't have to close)
        with open('config.csv', 'w', encoding='UTF8', newline='') as f:
            # inform user
            print(str(devices) + " devices will be generated...")

            # Create the writer 
            writer = csv.writer(f)

            # Write the header
            writer.writerow(header)

            while(counter != devices):
                data = [counter, '', randomBandwidth()]
                writer.writerow(data)
                counter += 1

if __name__ == '__main__':
    generateCSV()

