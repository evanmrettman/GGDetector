import json
import time
import requests
import utility.logging as log

# given a list of appids, request 1 app from the list each second until all apps are requested.
def requestEachApp(appids):
    count = 0
    for app in appids:
        
        count = count + 1
    print(count)

def requestApp(appid):
    wait_increase = 0
    req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
    while(req.status_code != requests.codes["ok"]): #This loop will be necassary to check if a request failed or not.
        print("Request on %d failed! Waiting %d seconds before next request..." % (appid, (10.01 + wait_increase)))
        time.sleep(10.01+wait_increase) #Steam allows only 10 requests every 10 seconds, if a call fails, I don't want to be marked as a DDOS, so wait the full 10 + .01
        wait_increase = wait_increase + 10
        req = requests.get('https://store.steampowered.com/api/appdetails?appids=%d' % (appid))
    print(req.json())
