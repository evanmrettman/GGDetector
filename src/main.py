#import antigravity
import utility.logging as log
import json
import files.parse as parse
import files.request as request
import requests


VERSION = 0
F_IN = "data"
F_ADD = "%s/additional_files" % F_IN
F_OUT = "output/v_%02d" % VERSION

F_IN_LIST = "list_short.json"
#F_IN_LIST = "list_4_26_19.json"

def main():
    log.info("Hello from Steam Sensor")


    #applist = parse.parseApps("%s/list_4_26_19.json" % (F_IN))

    applist = parse.parseApps("%s/%s" % (F_IN,F_IN_LIST))
    
    request.requestEachAppToCSV(applist,"%s_%s" % (F_IN, F_IN_LIST))

    # Test requests here
    #rtest = requests.get('https://store.steampowered.com/api/appdetails?appids=239350')
    #while(rtest.status_code != requests.codes["ok"]): #This loop will be necassary to check if a request failed or not.
    #    print("Request Error!")
    #    rtest = requests.get('https://store.steampowered.com/api/appdetails?appids=239350')
    #print(rtest.json())

if __name__ == "__main__":
    log.starting()
    main()
    log.ending()