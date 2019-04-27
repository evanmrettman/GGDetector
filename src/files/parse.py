import json
import objects.app_entry as AppEntry

def parseApps(fileLocation):
        with open(fileLocation, "r", encoding="utf8") as f:
                loaded_json = json.loads(f.read())
                #print(f.read())

         # below is a debug loop to print the json file.       
        for x in loaded_json:
                print(loaded_json[x])
                #print(x)
        #print(loaded_json["applist"])