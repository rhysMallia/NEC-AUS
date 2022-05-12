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
import sys, json, subprocess
import time
import pandas as pd
import hashlib as hash
import datetime

#constants
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
        variableDict = pd.read_csv(filename, header=None, skiprows=1, usecols=range(1,3))
        #print(variableDict)
        if variableDict.empty:
            # if the dict is empty, try to locate another file
            print("Unable to locate default config file.")
            print("Please enter the filename: ")
            temp = input().strip().lower()
            filename = temp + extension
        else:
            # if the dict is full, we can exit the loop
            # variableDict = variableDict.to_dict()
            #print(variableDict)
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
    
    # Iterate over every row and create the variables before launching the playbook
    for rows in range(0, rows):
        # Router description
        desc = variableDict[1][rows]
        # Bandwidth of connection
        bandwidth = variableDict[2][rows]
        # Dict to turn into JSON
        variableHolder = {}
        
        ## CE
        # Hostname (ex. CE001)
        hostname = createHost(count)
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
        # Interface (ex. 101, 102)
        interface += 1
        # PE Address (ex. 10.255.0.9)

        # PE Address 2 (ex. 10.255.0.13)

        # Tunnel (ex. 10.2555.0.10)

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

        variableHolder['interface'] = str(interface) 
        variableHolder['peaddress'] = ""
        variableHolder['peaddress2'] = ""
        variableHolder['tunnel'] = ""
        #print(variableHolder)
        
        # Convert dict object to json
        variableHolder = json.dumps(variableHolder)


        # Send object to run ansible command
        result = subprocess.run(
            [ansible, playbook, vars, variableHolder],
            capture_output = True, text = True
        )

        # print the stdout and error to the console
        print("stdout: " + result.stdout)
        #print("stderr: " + result.stderr)

        result = subprocess.run(
            [ansible, pePlaybook, vars, variableHolder],
            capture_output = True, text = True
        )
        print("stdout: " + result.stdout)
        #print("stderr: " + result.stderr)
        
        # Iterate nessicary counters
        if ipAddr >= 250:
            ipRange += 1
            #ipAddr = 1
        else:
            ipAddr += 1
        
        interface += 1
        count += 1

# This function will ensure that the hostname will always be 3 digits with leading zeros
def createHost(count):
    count = str(count)

    hostname = defaultHost

    while(len(count) < 3):
        count = "0" + count
    return hostname + count



if __name__ == "__main__":
    main()
