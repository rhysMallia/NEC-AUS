# TO DO (RHYS)
# PE CONFIG GENERATION
# ADD TUNNEL INFORMATION
# GENERATE DESC
# NETBOX IP(?)
#
#

# TO DO (CHU)
# LOGGING
#   HOW LONG THIS SCRIPT TAKES TO RUN
#   HOW MANY TIMES THIS HAS RUN
#   TOTAL TIME SAVED

# Module imports
import csv
import sys, json, subprocess
import time
import pandas as pd
import hashlib as hash
import datetime
import time

# constants
defaultFileName = "config"
extension = ".csv"
defaultHost = "CE"
secondaryHost = "PE"
ip = "172.28."
tunnel = "10.255."
ansible = "ansible-playbook"
playbook = "router.yml"
pePlaybook = "PE.yml"
vars = "--extra-vars"
variableDict = {}
variableArray = []
folder = ""
results = []
ceDesc = "This device is fanstastic, truly, this device is one of the best, and built right here ..."

def main(): 
    t_start = time.perf_counter()
    fileInput()
    generateFolder()
    executeScript()
    t_end = time.perf_counter()
    print(f"script time: { t_end - t_start} seconds")
    
# Checks if the file is present, if not asks for user imput
def fileInput():
    # read default file    
    filename = defaultFileName + extension
    check = False
    while not check:
        global variableDict
        variableDict = pd.read_csv(filename, header=None, skiprows=1, usecols=range(1, 3))
        if variableDict.empty:
            # if the dict is empty, try to locate another file
            print("Unable to locate default config file.")
            print("Please enter the filename: ")
            temp = input().strip().lower()
            filename = temp + extension
        else:
            # if the dict is full, we can exit the loop
            # variableDict = variableDict.to_dict()
            check = True


# Generates a tailored folder to paste the generated CSV files
def generateFolder():
    global folder
    # get the date time 
    x = datetime.datetime.now()

    # Convert into usable format and set as the global variable
    folder = x.strftime("%H%M%d%B%Y")


# Generates the variables and sends them to the ansible playbook
def executeScript():
    global variableDict
    global folder

    # Count maintains which device is currently being used
    count = 1
    # Tunnel goes from 101 to 600
    tunnelCount = 101
    # IP range goes from 0 to 1 when IP address increases above 250 (Keep some IPs for devices)
    ipRange = 0
    # IP address goes from 1 to 250
    ipAddr = 1
    # The length of the dict show us how many rows
    rows = len(variableDict)
    # Interface counter
    interface = 100
    #Prefix
    prefixAddr = 1
    # Prefix range
    prefixRange = 0

    # Iterate over every row and create the variables before launching the playbook
    for rows in range(0, rows):
        # Start timer
        start = time.perf_counter()
        # Router description
        desc = ceDesc
        # Bandwidth of connection
        bandwidth = variableDict[1][rows]
        # Dict to turn into JSON
        variableHolder = {}
        
        ## Ethernet and Tunnel Prefixes
        # Ethernet Prefix
        peEth = str(tunnel) + str(prefixRange) + str(prefixAddr)   
        ceEth = str(tunnel) + str(prefixRange) + str(prefixAddr + 1)
        # Tunnel Prefix
        peTun = str(tunnel) + str(prefixRange) + str(prefixAddr + 4)
        ceTun = str(tunnel) + str(prefixRange) + str(prefixAddr + 5)

        ## CE
        # Hostname (ex. CE001, PE001)
        hostname = createHost(count, True)
        # Shape Averages THIS ISN'T WORKING 100%
        shapeAvg1 = int((bandwidth * 10**5) * 0.97)
        shapeAvg2 = int((bandwidth * 10**3) * 0.97)
        # Policy Maps (ex. 10MB)
        policy = str(bandwidth) + "MB"
        # IP address (ex. 192.168.88.1)
        ipAddress = ip + str(ipRange) + "." + str(ipAddr) 
        # tunnel bandwidth (ex. 1000000)
        tunnelBandwidth = int((bandwidth * 10**3))
        # MD5 Hash (ex. 001100101001md)
        temp = (hostname + desc + str(ipAddress) + str(bandwidth))
        digestKey = hash.md5(temp.encode('utf-8')).hexdigest()
       
        ## PE
        # Hostname
        hostname2 = createHost(count, False)
        # Count
        # Interface (ex. 101, 102)
        interface += 1
        
        # Add to Dict object
        variableHolder['hostname'] = str(hostname)
        variableHolder['bandwidth'] = str(bandwidth)
        variableHolder['desc'] = str(desc)
        variableHolder['ipaddress'] = str(ipAddress)
        variableHolder['shapeAvg1'] = str(shapeAvg1)
        variableHolder['shapeAvg2'] = str(shapeAvg2)
        variableHolder['policy'] = str(policy)
        variableHolder['digestKey'] = str(digestKey)
        variableHolder['folder'] = str(folder)
        variableHolder['ceEth'] = str(ceEth)
        variableHolder['ceTun'] = str(ceTun)
        
        variableHolder['hostname2'] = str(hostname2)
        variableHolder['count'] = str(count)
        variableHolder['interface'] = str(interface) 
        variableHolder['peEth'] = str(peEth)
        variableHolder['peTun'] = str(peTun)
        #print(variableHolder)
        
        # Convert dict object to json
        variableHolder = json.dumps(variableHolder)

        # Print statements for testing
        print("Generating CE configuration files for device no." + str(count) )
        # Send object to run ansible command
        result = subprocess.run(
            [ansible, playbook, vars, variableHolder],
            capture_output=True, text=True
        )

        # print the stdout and error to the console
        print("stdout: " + result.stdout)
        #print("stderr: " + result.stderr)
        
        # Print statements for testing
        print("Generating PE configuration files for device no." + str(count) )
        result = subprocess.run(
            [ansible, pePlaybook, vars, variableHolder],
            capture_output = True, text = True
        )
        print("stdout: " + result.stdout)
        
        # Iterate nessicary counters and perform checks that they are within bounds
        if ipAddr >= 250:
            ipRange += 1
            ipAddr = 1
        else:
            ipAddr += 1
        
        interface += 1
        count += 1

        prefixAddr += 8
        if prefixAddr >= 250:
            prefixRange += 1
            prefixAddr = 1

        # Time the individual runs
        print(benchmark(hostname, start))
    # Time the total run time
    print(benchmark_output(count))


# This function will ensure that the hostname will always be 3 digits with leading zeros
def createHost(count, check):
    count = str(count)

    hostname = defaultHost

    while (len(count) < 3):
        count = "0" + count

    if check:    
        return hostname + count
    else:
        return secondaryHost + count

def benchmark(hostname, start):
    timelapse = time.perf_counter() - start
    result = [hostname, timelapse]
    results.append(result)
    return f'config {hostname} generated, timelapse: {timelapse:.4f} seconds'


def benchmark_output(count):
    with open('benchmark.csv', 'w', newline='') as file:
        write_head = csv.writer(file, delimiter=',')
        write_head.writerows(results)
    total = 0
    for x in results:
        total = total + x[1]

    return f'total time:{total:.4f} seconds ,average time:{total/count:.4f} seconds'


if __name__ == "__main__":
    main()
