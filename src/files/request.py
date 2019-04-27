import json
import time
import requests
import datetime
import math
import utility.logging as log
import files.parse as parse

F_OUT_JSON = "data/output/appinfo.json"
F_OUT_ERROR = "data/output/errorids.json"

# given a list of appids, request 1 app from the list each second until all apps are requested.
def requestEachAppToCSV(appids,filepath):


    allApps = [] #DEBUG


    count = 0
    total = len(appids["applist"]["apps"]["app"])
    numberOfMessages = math.ceil(total/5)
    name = "Requesting data and writing to CSV file..."

    start = time.time()
    end = time.time()
    delta = (end - start)

    parse.createJSON(F_OUT_JSON) # start the JSON file

    log.processing(name)
    for app in appids["applist"]["apps"]["app"]:

        # deal with time
        end = time.time() # end timer
        delta = (end-start) # record delta
        # API request limit: 10 per 10 seconds, 200 per 5 minutes (I'll abide by this one, which is 1 per 1.5 seconds), 100,000 per day (this is bigger than needed).
        if(delta <= 1.501): 
            time.sleep(1.501 - delta) # delay to avoid throttling (try to ensure 1.501 seconds between each request)

        # request app
        tempApp = requestApp(app["appid"])
        # start timer
        start = time.time()



        # print(tempApp)


        log.sofar(name,count,total,numberOfMessages)
        count = count + 1

        #allApps.append(requestApp(app["appid"])) #DEBUG REMOVE BEFORE RUNNING ON REAL DATA TO AVOID NOMEM ERROR <------- REMOVE -- REMOVE -- REMOVE -- REMOVE -- REMOVE!!!
        # Now write to a CSV file
        
        parse.appendJSON(F_OUT_JSON,tempApp,count) # COMMENT THIS BACK IN

        # Sleep
        if(delta >= 1.001): 
            time.sleep(1.001 - delta) # delay to avoid DDOS detection
        
        # Now request the app
    
    parse.endJSON(F_OUT_JSON) # end the JSON file

    time.sleep(3) # Debug, remove this later
    #print(allApps)
    print(count)

def requestApp(appid):
    wait_increase = 0
    req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
    while(req.status_code != requests.codes["ok"] and wait_increase < 1000): #This loop will be necassary to check if a request failed or not.
        print("Request on %d failed! Waiting %d seconds before next request..." % (appid, (10.01 + wait_increase)))
        time.sleep(10.01+wait_increase) # Steam allows only 200 requests every 5 minutes, if a call fails, I don't want to be marked as a DDOS, so after two fails, wait the full 5
        wait_increase = wait_increase * 2 # by this point I have probably hit the daily limit, so this is kind of pointless
        if(wait_increase < 300):
            req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
        else:
            parse.appendERROR(F_OUT_ERROR, appid)
    #print(req.json())

    return req.json()
