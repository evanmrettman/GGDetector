import json
import time
import requests
import datetime
import math
import utility.logging as log
import parse as parse

# given a list of appids, request 1 app from the list each second until all apps are requested.
def requestEachAppToCSV(appids,filepath):


    allApps = [] #DEBUG


    count = 0
    total = len(appids["applist"]["apps"]["app"])
    numberOfMessages = 20
    name = "Requesting data and writing to CSV file..."

    start = time.time()
    end = time.time()
    delta = (end - start)

    log.processing(name)
    for app in appids["applist"]["apps"]["app"]:

        # deal with time
        end = time.time() # end timer
        delta = (end-start) # record delta
        if(delta >= 1.001): 
            time.sleep(1.001 - delta) # delay to avoid DDOS detection (try to ensure 1.01 seconds between each request)

        # request app
        tempApp = requestApp(app["appid"])
        # start timer
        start = time.time()


        log.sofar(name,count,total,numberOfMessages)
        count = count + 1

        #allApps.append(requestApp(app["appid"])) #DEBUG REMOVE BEFORE RUNNING ON REAL DATA TO AVOID NOMEM ERROR <------- REMOVE -- REMOVE -- REMOVE -- REMOVE -- REMOVE!!!
        # Now write to a CSV file
        parse.appendCSV(filepath,tempApp)

        # Sleep
        if(delta >= 1.001): 
            time.sleep(1.001 - delta) # delay to avoid DDOS detection
        
        # Now request the app
    
    time.sleep(3) # Debug, remove this later
    #print(allApps)
    print(count)

def requestApp(appid):
    wait_increase = 0
    req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
    while(req.status_code != requests.codes["ok"]): #This loop will be necassary to check if a request failed or not.
        print("Request on %d failed! Waiting %d seconds before next request..." % (appid, (10.01 + wait_increase)))
        time.sleep(10.01+wait_increase) #Steam allows only 10 requests every 10 seconds, if a call fails, I don't want to be marked as a DDOS, so wait the full 10 + .01
        wait_increase = wait_increase + 5
        req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
    #print(req.json())

    return req.json()
