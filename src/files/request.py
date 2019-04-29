import json
import time
import requests
import datetime
import math
import utility.logging as log
import files.parse as parse

F_OUT_JSON = "data/output/apps/" # HAVE TO ADD POSTFIX .json IN PARSE
F_OUT_ERROR = "data/output/errorids.json"

# given a list of appids, request 1 app from the list each second until all apps are requested.
def requestEachAppToJSON_SteamAPI(appids,filepath): # 
    # API request limit: 10 per 10 seconds, 200 per 5 minutes (I'll abide by this one, which is 1 per 1.5 seconds), 100,000 per day (this is bigger than needed).

    count = 0
    total = len(appids["applist"]["apps"]["app"])
    numberOfMessages = math.ceil(total/5)
    name = "Requesting data and writing to JSON file..."
    start = time.time()
    end = time.time()
    delta = (end - start)

    log.processing(name)
    for app in appids["applist"]["apps"]["app"]:
        if count <= 68760:
            count += 1
            continue

        end = time.time() # end timer
        delta = (end-start) # record delta

        if(delta <= 1.501): 
            time.sleep(1.501 - delta) # delay to avoid throttling (try to ensure 1.501 seconds between each request)

        tempApp = requestAppSteamAPI(app["appid"]) # Request the app from steam api
        start = time.time() # Start the timer.
        log.sofar(name,count,total,numberOfMessages)
        count = count + 1
        parse.writeJSON(F_OUT_JSON,tempApp,count,app["appid"])

    time.sleep(3) # Debug, remove this later

# given a list of appids, request 1 app from the list each second until all apps are requested.
def requestEachAppToJSON_SteamAPI(appids): # 
    # API request limit: 10 per 10 seconds, 200 per 5 minutes (I'll abide by this one, which is 1 per 1.5 seconds), 100,000 per day (this is bigger than needed).

    count = 0
    total = len(appids["applist"]["apps"]["app"])
    numberOfMessages = math.ceil(total/5)
    name = "Requesting data and writing to JSON file..."
    limit = 1/4 + 0.1 # 4 calls per second with 0.1 seconds of lee-way per call
    start = time.time()
    end = time.time()
    delta = (end - start)

    log.processing(name)
    for app in appids["applist"]["apps"]["app"]:
        if count <= -1:
            count += 1
            continue

        end = time.time() # end timer
        delta = (end-start) # record delta

        if(delta <= limit): 
            time.sleep(limit - delta) # delay to avoid throttling (try to ensure 1.501 seconds between each request)

        tempApp = requestAppSteamSpy(app["appid"]) # Request the app from steam api
        start = time.time() # Start the timer.
        log.sofar(name,count,total,numberOfMessages)
        count = count + 1
        parse.writeJSON("data/output/steamspy/",tempApp,count,app["appid"])

    time.sleep(3) # Debug, remove this later

def requestAppSteamSpy(appid):
    api_link = 'http://steamspy.com/api.php?request=appdetails&appid=%d' % (appid)
    wait_increase = 0
    req = requests.get(api_link)
    while(req.status_code != requests.codes["ok"] and wait_increase < 1000): #This loop will be necassary to check if a request failed or not.
        log.info("Request on %d failed! Waiting %d seconds before next request..." % (appid, (10.01 + wait_increase)))
        time.sleep(10.01+wait_increase) # Steam allows only 200 requests every 5 minutes, if a call fails, I don't want to be marked as a DDOS, so after two fails, wait the full 5
        wait_increase = wait_increase * 2 # by this point I have probably hit the daily limit, so this is kind of pointless
        if(wait_increase < 300):
            req = requests.get(api_link)
        else:
            parse.appendERROR(F_OUT_ERROR, appid)
    return req.json()

def requestAppSteamAPI(appid):
    wait_increase = 0
    req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
    while(req.status_code != requests.codes["ok"] and wait_increase < 1000): #This loop will be necassary to check if a request failed or not.
        log.info("Request on %d failed! Waiting %d seconds before next request..." % (appid, (10.01 + wait_increase)))
        time.sleep(10.01+wait_increase) # Steam allows only 200 requests every 5 minutes, if a call fails, I don't want to be marked as a DDOS, so after two fails, wait the full 5
        wait_increase = wait_increase * 2 # by this point I have probably hit the daily limit, so this is kind of pointless
        if(wait_increase < 300):
            req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
        else:
            parse.appendERROR(F_OUT_ERROR, appid)
    return req.json()
