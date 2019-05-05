#import antigravity
import utility.logging as log
import json
import time
import files.parse as parse
import files.request as request
import pproc.pproc as pp
import plots.plot as plt
import classifier.classifier as clf
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
        limit_input = True
        limit_value = 5000

        log.processing("Gathering JSON Dictionaries from Files")
        apps = parse.readDirectoryJSON(F_APPS,lim=limit_input,lim_value=limit_value)
        log.info("Gathered %d app data." % len(apps))
        
        log.processing("Converting JSON data to Game Objects")
        games = pp.CreateGames(apps)
        log.info("%d games created." % len(games))

        log.processing("Gathering SteamSpy JSON Dictionaries from files")
        spy = parse.readDirectoryJSON(F_SPY,lim=limit_input,lim_value=limit_value)
        log.info("Gathered %d steamspy data." % len(spy))

        log.processing("Adding SteamSpy JSON data to Game Objects")
        pp.ProcessAddSteamSpy(spy,games)

        # Remove old games from the list
        old_len = len(games)
        yearlimit = 2018
        log.processing("Removing games that are older than the year %d." % yearlimit)
        games = pp.getRecentGames(games, yearlimit)
        log.info("Removed %d games from list of %d. %d games are left." % (old_len-len(games),old_len,len(games)))

        log.processing("Creating list of keys for components in vectorization")
        all_platforms = pp.getPlatforms(games)
        all_categories = pp.getCategories(games)
        all_developers = pp.getDevelopers(games)
        all_publishers = pp.getPublishers(games)
        all_genres = pp.getGenres(games)
        all_langs = pp.getLanguages(games)
        all_tags = pp.getTags(games)
        log.info("%d vector data entries created." % (len(all_platforms)+len(all_categories)+len(all_developers)+len(all_publishers)+len(all_genres)+len(all_langs)+len(all_tags)))



        if False:
            log.info("plats")
            log.info(all_platforms)
            log.info("those were plats")
            time.sleep(1)
            log.info("cats")
            log.info(all_categories)
            log.info("those were cats")
            time.sleep(1)
            log.info("devs")
            log.info(all_developers)
            log.info("those were devs")
            time.sleep(1)
            log.info("pubs")
            log.info(all_publishers)
            log.info("those were pubs")
            time.sleep(1)
            log.info("genres")
            log.info(all_genres)
            log.info("those were genres")
            time.sleep(1)
            log.info("langs")
            log.info("those were langs")
            log.info(all_langs)
            time.sleep(1)
            log.info("tags")
            log.info(all_tags)
            log.info("those were tags")

        log.processing("Vectorizing games")
        vectors = []
        for i, game in enumerate(games.values()):
            vectors.append(game.vectorize(all_platforms,all_categories,all_developers,all_publishers,all_genres,all_langs,all_tags))
            log.sofar("Vectorizing Games", i, len(games), 10)

        log.processing("Making Graphs")
        plt.createGameGraphs(F_OUT,games)

        log.processing("Testing Classifiers")
        clf.testClassifiers(F_OUT,games,show=True)#,TestKNN=False,TestNNetwork=False,TestNBayes=False,TestDTree=False,TestRForest=False)



if __name__ == "__main__":
    log.starting()
    main()
    log.ending()