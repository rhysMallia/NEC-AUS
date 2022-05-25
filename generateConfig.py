import csv
import random
import sys

counter = 1
header = ['No', ' ', 'bandwidth (MB)']
bandwidth = [10, 20, 50, 100, 200, 300, 500, 1000]

def randomBandwidth():
    global bandwidth
    return bandwidth[random.randrange(0, len(bandwidth), 1)]

def generateCSV(amount):
    global counter
    global header
# check for extra vars
    # open the file ( with keyword means you don't have to close)
    with open('config.csv', 'w', encoding='UTF8', newline='') as f:
        # inform user
        print(str(amount) + " devices will be generated...")

        # Create the writer 
        writer = csv.writer(f)

        # Write the header
        writer.writerow(header)

        while(counter >= amount):
            data = [counter, '', randomBandwidth()]
            writer.writerow(data)
            counter += 1

if __name__ == '__main__':
    generateCSV()

