import json
import csv
import os
import objects.app_entry as AppEntry

# parses and loads an applist json which is then returns
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