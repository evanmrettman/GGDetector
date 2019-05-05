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
import sys

VERSION = 4
F_IN = "data"
F_APPS = "%s/output/apps/" % F_IN
F_SPY = "%s/output/steamspy/" % F_IN
F_TEST_INPUT = "%s/input/" % F_IN
F_OUT = "output/v_%02d" % VERSION
F_OUT_JSON = "data/output/appinfo.json"
F_OUT_ERROR = "data/output/errorids.json"

#F_IN_LIST = "list_short.json"
F_IN_LIST = "list_4_26_19.json"

def main():

    pos_ratio = 0.5
    if len(sys.argv) >= 2:
        try:
            try: # check if it is a float
                float(sys.argv[1])
            except ValueError:
                raise Exception("Command line argument for classifier ratio is not a numerical value.")
            pos_ratio = float(sys.argv[1])
            if pos_ratio <= 0 or pos_ratio >= 1: # check if its a valid range
                raise Exception("Command line argument for classifier ratio is not within (0,1) range.")
        except Exception as e:
            log.info(e) # we raised an error, print it for understanding
            return # leave because we failed with the command line argument

    log.info("Running program with positive ratio classifier limit of %3.2f%%." % (pos_ratio*100))

    limit_input = False
    limit_value = 1000
    GetTestingData = False
    SteamAPI = False
    SteamSpy = False
    TestInput = True
    MakeGraphs = False
    TestClassifiers = False
    NumberOfTestInputs = 2
    GenerateGames = True
    NumberOfGenerated = 1000

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
        apps = parse.readDirectoryJSON(F_APPS,lim=limit_input,lim_value=limit_value)
        log.info("Gathered %d app data." % len(apps))
        
        log.processing("Converting JSON data to Game Objects")
        games = pp.CreateGames(apps,pos_ratio)
        log.info("%d games created." % len(games))

        log.processing("Gathering SteamSpy JSON Dictionaries from files")
        spy = parse.readDirectoryJSON(F_SPY,lim=limit_input,lim_value=limit_value)
        log.info("Gathered %d steamspy data." % len(spy))

        log.processing("Adding SteamSpy JSON data to Game Objects")
        pp.ProcessAddSteamSpy(spy,games)

        # Remove old and irrelevant games from the list
        old_len = len(games)
        yearlimit = 2018
        review_min = 200
        log.processing("Removing games that are older than the year %d." % yearlimit)
        games = pp.getRecentGames(games, yearlimit)
        log.info("Removed %d games from list of %d. %d games are left." % (old_len-len(games),old_len,len(games)))
        log.processing("Removing games that have less than than %d reviews." % review_min)
        games = pp.getRelevantGames(games, review_min)
        log.info("Removed %d games from list of %d. %d games are left." % (old_len-len(games),old_len,len(games)))
        

        log.processing("Creating list of keys for components in vectorization")
        all_platforms = pp.getPlatforms(games)
        all_categories = pp.getCategories(games)
        all_developers = pp.getDevelopers(games,mini=10)
        all_publishers = pp.getPublishers(games,mini=10)
        all_tags = pp.getTags(games,mini=5000)
        all_genres = pp.getGenres(games)
        all_langs = pp.getLanguages(games)
        log.info("%d vector data entries created." % 
        (len(all_platforms)+len(all_categories)+len(all_developers)+len(all_publishers)+len(all_genres)+len(all_langs)+len(all_tags)))

        log.processing("Vectorizing games")
        vectors = []
        for i, game in enumerate(games.values()):
            vectors.append(game.vectorize(
                all_platforms,
                all_categories,
                all_developers,
                all_publishers,
                all_genres,
                all_langs,
                all_tags
                ))
            log.sofar("Vectorizing Games", i, len(games), 10)

        # Load input here
        test_games = []
        if TestInput:
            log.info("Loading input games...")
            for x in range(NumberOfTestInputs):
                test_game = pp.inputGame(parse.readJSON("%sinput%d.json" % (F_TEST_INPUT, x)))
                test_vector = test_game.vectorize(all_platforms,all_categories,all_developers,all_publishers,all_genres,all_langs,all_tags)
                test_games.append(test_game)
        
        # Generate test games here
        if GenerateGames:
            log.info("Generating random test games...")
            for x in range(NumberOfGenerated):
                test_game = pp.inputGame(pp.generateRandomGame(all_platforms,all_categories,all_developers,all_publishers,all_genres,all_langs,all_tags))
                test_game.vectorize(all_platforms,all_categories,all_developers,all_publishers,all_genres,all_langs,all_tags)
                test_games.append(test_game)

        if MakeGraphs:
            log.processing("Making Graphs")
            plt.createGameGraphs(F_OUT,games)

        if TestClassifiers:
            log.processing("Testing Classifiers")
            clf.testClassifiers(F_OUT,games,pos_ratio,sampleperc=0.7,show=False)#,TestKNN=False,TestNNetwork=False,TestNBayes=False,TestDTree=False,TestRForest=False)

        if MakeGraphs:
            log.processing("Creating Classifier Data Graphs")
            plt.createClassifierGraphs(F_OUT,"%s/classifier_data/" % F_OUT)

        log.processing("Classifying Test Games")
        clf.predict(F_OUT,games,test_games)

if __name__ == "__main__":
    log.starting()
    main()
    log.ending()