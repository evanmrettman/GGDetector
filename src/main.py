#import antigravity
import utility.logging as log
import json
import files.parse as parse
import files.request as request
import requests
import pproc.pproc as pp

VERSION = 0
F_IN = "data"
F_APPS = "%s/output/apps/" % F_IN
F_OUT = "output/v_%02d" % VERSION
F_OUT_JSON = "data/output/appinfo.json"
F_OUT_ERROR = "data/output/errorids.json"

#F_IN_LIST = "list_short.json"
F_IN_LIST = "list_4_26_19.json"

def main():

    GetTestingData = False
    SteamAPI = False
    SteamSpy = False

    if GetTestingData:
        log.processing("Gathering Application List")
        applist = parse.parseApps("%s/%s" % (F_IN,F_IN_LIST))
        log.info("Retrieved %d apps." % len(applist))

        if SteamAPI:
            log.processing("Requesting AppsIDs from Steam API")
            request.requestEachAppToJSON_SteamAPI(applist,"%s_%s" % (F_IN, F_IN_LIST))
        if SteamSpy:
            log.processing("Requesting AppIds from Steam Spy")
            request.requestEachAppToJSON_SteamAPI(applist)
    else:
        log.processing("Gathering JSON Dictionaries from Files")
        apps = parse.readDirectoryJSON(F_APPS)
        log.info("Gathered %d app data." % len(apps))
        
        log.processing("Converting JSON data to Game Objects")
        games = pp.CreateGames(apps)
        log.info("Created %d game objects." % len(games))
        for game in games.values():
            log.info(game.string())


if __name__ == "__main__":
    log.starting()
    main()
    log.ending()