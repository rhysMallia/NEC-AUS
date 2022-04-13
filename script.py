# TO DO
#
#
#
#

# Module imports
import sys, json, subprocess
import pandas as pd
import hashlib as hash

#constants
defaultFileName = "config"
extension = ".csv"
defaultHost = "CE"
ip = "172.28."
tunnel = "10.255."
ansible = "ansible-playbook"
playbook = "router.yml"
vars = "--extra-vars"
variableDict = {}
variableArray = []

def main():
    #Either take user input, or begin scanning CSV
    fileInput()
    executeScript()

    # For loop, set up varibles to send to 
    
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

def executeScript():
    global variableDict

    # Count maintains which device is currently being used
    count = 1
    # Tunnel goes from 101 to 600
    tunnelCount = 101
    # IP range goes from 0 to 1 when IP address increases above 250 (Keep some IPs for devices)
    ipRange = 0
    # IP address goes from 1 to 250
    ipAddr = 1

    #print(variableDict)
    #for index, row in variableDict.iterrows():
    # [row][column]
    rows = len(variableDict)
    
    for rows in range(0, rows):
        # Router description
        desc = variableDict[1][rows]
        # Bandwidth of connection
        bandwidth = variableDict[2][rows]
        # Dict to turn into JSON
        variableHolder = {}
        #print(desc)
        #print(bandwidth)
        
        # Hostname
        hostname = createHost(count)
        # Shape Averages THIS ISN'T WORKING 100%
        shapeAvg1 = int((bandwidth * 10**5) * 0.97)
        shapeAvg2 = int((bandwidth * 10**3) * 0.97)
        # Policy Maps
        policy = str(bandwidth) + "MB"
        # IP address
        ipAddress = ip + str(ipRange) + "." + str(ipAddr) 
        # tunnel bandwidth
        tunnelBandwidth = int((bandwidth * 10**3))
        # MD5 Hash
        temp = (hostname + desc + str(ipAddress) + str(bandwidth))
        digestKey = hash.md5(temp.encode('utf-8')).hexdigest()
        
        # Testing prints
        #print(bandwidth)
        #print(desc)
        #print(shapeAvg1)
        #print(shapeAvg2)
        #print(policy)
        #print(ipAddress)
        #print(digestKey)
        
        # Add to Dict object
        #variableHolder['bandwidth'] = 1
        variableHolder['bandwidth'] = str(bandwidth)
        variableHolder['desc'] = str(desc)
        variableHolder['ipaddress'] = str(ipAddress)
        variableHolder['shapeAvg1'] = str(shapeAvg1)
        variableHolder['shapeAvg2'] = str(shapeAvg2)
        variableHolder['policy'] = str(policy)
        variableHolder['digestKey'] = str(digestKey)

        print(variableHolder)
        # Convert dict object to json
        variableHolder = json.dumps(variableHolder)


        # Send object to run ansible command
        result = subprocess.run(
            [ansible, playbook, vars, variableHolder],
            capture_output = True, text = True
        )

        # print the stdout and error to the console
        print("stdout: " + result.stdout)
        print("stderr: " + result.stderr)

        # Iterate nessicary counters
        if ipAddr >= 250:
            ipRange += 1
            ipAddr = 1
        else:
            ipAddr += 1
        count += 1

def createHost(count):
    count = str(count)
    hostname = defaultHost

    while(len(count) < 3):
        count = "0" + count
    return hostname + count


if __name__ == "__main__":
    main()