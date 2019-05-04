#import antigravity
import utility.logging as log
import json
import time
import files.parse as parse
import files.request as request
import requests
import pproc.pproc as pp
import plots.plot as plt
from collections import defaultdict

VERSION = 0
F_IN = "data"
F_APPS = "%s/output/apps/" % F_IN
F_SPY = "%s/output/steamspy/" % F_IN
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
        log.info("%d games created." % len(games))

        log.processing("Gathering SteamSpy JSON Dictionaries from files")
        spy = parse.readDirectoryJSON(F_SPY)
        log.info("Gathered %d steamspy data." % len(spy))

        log.processing("Adding SteamSpy JSON data to Game Objects")
        for data in spy:
            if data["appid"] in games.keys():
                games[data["appid"]].addSteamSpyData(data)

        log.processing("Creating list of keys for components in vectorization")
        all_platforms = pp.getPlatforms(games)
        all_categories = pp.getCategories(games)
        all_developers = pp.getDevelopers(games)
        all_publishers = pp.getPublishers(games)
        all_genres = pp.getGenres(games)
        all_langs = pp.getLanguages(games)
        all_tags = pp.getTags(games)

        #debug
        log.info("plats")
        log.info(all_platforms)
        log.info("those were plats")
        time.sleep(2)
        log.info("cats")
        log.info(all_categories)
        log.info("those were cats")
        time.sleep(2)
        log.info("devs")
        log.info(all_developers)
        log.info("those were devs")
        time.sleep(2)
        log.info("pubs")
        log.info(all_publishers)
        log.info("those were pubs")
        time.sleep(2)
        log.info("genres")
        log.info(all_genres)
        log.info("those were genres")
        time.sleep(2)
        log.info("langs")
        log.info("those were langs")
        log.info(all_langs)
        time.sleep(2)
        log.info("tags")
        log.info(all_tags)
        log.info("those were tags")

        log.processing("Vectorizing games")
        vectors = []
        #log.info("DEBUG")
        #log.info(games)
        count = 0
        for game in games.values():
            count += 1
            #log.info("DEBUG")
            #log.info(game.string())
            #for lang in game.get_supported_languages():
            #    log.info(lang)
            vectors.append(game.vectorize(all_platforms,all_categories,all_developers,all_publishers,all_genres,all_langs,all_tags))
            log.sofar("vectorizing games", count, len(games), 100)

        log.info(vectors[5])

        # I want to see how many tags there are
        #tags = defaultdict(int)
        #for game in games.values():
        #    if len(game.get_tags()) != 0:
        #        for key, value in game.get_tags().items():
        #            tags[key] += value


        
        #log.info("PRINTING TAGS WITH OVER 1000 USES")
        #for tag, value in tags.items():
        #    if(value > 1000):
        #        log.info("%s:%d" % (tag,value))
        
        # vectorize games
        # first retrieve list of all possible platforms, categories, genres, languages, and tags for vectorization


        log.processing("Making Graphs")
        plt.createGameGraphs(F_OUT,games)



if __name__ == "__main__":
    log.starting()
    main()
    log.ending()