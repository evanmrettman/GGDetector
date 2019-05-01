import json
import csv
import os
import objects.game as Game
import utility.logging as log

# parses and loads an applist json which is then returned
def parseApps(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        loaded_json = json.loads(f.read())
    return loaded_json

# treat all files in the given directory as json and parse them as such then return a list of dictionaries contianing the information
def readDirectoryJSON(directory):
    dicts = []
    dir_files = os.listdir(directory)
    for i, file in enumerate(dir_files):
        if False and i >= 5000: # debug: only grab a sample set for now
            break
        with open(directory+file, "r", encoding="utf8") as f:
            dicts.append(json.loads(f.readline()))
        log.sofar("Reading JSON files from %s" % directory,i,len(dir_files),100)
    return dicts

def readJSON(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        loaded_json = json.loads(f.read())

    count = 0
    for x in loaded_json["applist"]["apps"]["app"]:
        print("")
        print(x["appid"])
        print(x["name"])
        count = count + 1
    print(count)

    return loaded_json

def appendCSV(filepath,data):
    f = open(filepath,"a",newline='')
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()

def createCSV(filepath,data):
    f = open(filepath,"w",newline='')
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()

def writeDict(filepath,d):
    f = open(filepath,'w',newline='')
    writer = csv.writer(f)

    tempList = []
    for key in d.keys():
        tempList.append(key)

    writer.writerow(tempList)
    #writer.writerow(d[next(iter(d))].params())
    for v in d.values():
        writer.writerow(v.values())
    f.close()

def createJSON(filepath):
    f = open(filepath, 'w',newline='')
    f.write('{')
    #print('{')
    f.close()

def appendJSON(filepath, data, count):
    f = open(filepath,'a',newline='')
    if(count <= 1):
        f.write(' "count%d":' % (count))
    else:
        f.write(', "count%d":' % (count))
    json.dump(data, f)
    f.close()

def endJSON(filepath):
    f = open(filepath, 'a',newline='')
    f.write("}")
    #print('}')
    f.close()

def writeJSON(filepath,data,count,appid):
    f = open("%s%d_%d_app.json" % (filepath,count,appid), 'w',newline='')
    json.dump(data, f)
    f.close()

def appendERROR(filepath, count):
    f = open(filepath,'a',newline='')
    f.write('Error at appid: %d \n' % (count))
    f.close()