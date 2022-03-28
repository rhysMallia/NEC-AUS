# TO DO
# Clean inputs from user
# Ask user for name of playbook (?)

# Module imports
import sys, json, subprocess

# constants
valuedict = {"ip": "", "dns": "", "ip_range": ""}
ansiblestring = "ansible-playbook test.yml --extra-vars "

# This function will check if the user wants to continue
def usercheck():
    value = None
    while value != False:
        print("Continue? (Y/n): ")
        value = input().strip().lower()
        
        if value == "n":
            sys.exit()
        elif value == "y" or value == "":
            return

# This function will take inputs from the user and  create a json object 
# from the results, before passing the object to a ansible CLI command
def main():
    #for key, value in valuedict.items():
    for key in valuedict:
        print("Enter a value for " + key + ":")
        value = input().strip()

        if value == "":
            print("No value entered ... skipping ...")
        else:
            valuedict[key] = value

    # Check if the dict is correct
    print("The following has been recorded: ")
    print(valuedict)
    usercheck()

    # Remove empty values from the dict object
    #cleaneddict = list(filter(None, ({key : val for key, val in sub.items() if val} for sub in valuedict)))

    # convert the dict into a json string object
    ansibleobject = json.dumps(valuedict)
    print(ansibleobject)

    # run ansible with the json object 
    result = subprocess.run(
        #[ansiblestring + ansibleobject],
        ["ansible-playbook", "test.yml", "--extra-vars", "{'ip': '12'}"],
        capture_output = True, text = True, #shell = True #,check = True
    )

    # print the stdout and error to the console
    print("stdout: " + result.stdout)
    print("stderr: " + result.stderr)



    
if __name__ == "__main__":
    main()


    