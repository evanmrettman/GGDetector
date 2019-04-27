import json
import csv
import os
import objects.app_entry as AppEntry

def parseApps(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        loaded_json = json.loads(f.read())
        #print(f.read())

    # below is a debug loop to print the json file.
    #for x in loaded_json:
        #print(loaded_json[x])
        #print(x)
        #print(loaded_json["applist"])

    #for key in loaded_json.keys():
        #print(key)

    count = 0
    for x in loaded_json["applist"]["apps"]["app"]:
        print("")
        print(x["appid"])
        print(x["name"])
        count = count + 1
    print(count)

def appendCSV(filepath,data):
    f = open(filepath,"a",newline='')
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()