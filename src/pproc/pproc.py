import utility.logging as log
import random
from collections import defaultdict
from objects.game import Game
import math

def CreateGames(json_dicts,pos_ratio):
    games = defaultdict(Game)
    for i, steam_response in enumerate(json_dicts):
        appid = list(steam_response.keys())[0]
        inner_d = steam_response[appid]
        if inner_d["success"] == True:
            if inner_d["data"]["type"] == "game":
                games[int(appid)] = Game(steam_response,pos_ratio)
        log.sofar("Creating Games",i,len(json_dicts),10)
    return games

def inputGame(json):
    return Game(json, 0, True)

def ProcessAddSteamSpy(json_dicts, games):
    spy_dict_index = defaultdict(dict)
    for item in json_dicts:
        spy_dict_index[int(item["appid"])] = item
    for i, game in enumerate(games.values()):
        game.addSteamSpyData(spy_dict_index[game.get_id()])
        log.sofar("Adding steam spy data", i, len(games),4)

def generateRandomGame(plats, cats, devs, pubs, genres, langs, tags, seed = None):
    random.seed(seed)
    if seed == None:
        seed = random.randint(0,100000)
    random.seed(seed)
    randJSON = {"name": ("game-%d" % seed)}
    randJSON["id"] = seed
    randJSON["type"] = "game"

    randJSON["required_age"] = 0
    if (random.randint(0,1)):
        randJSON["required_age"] = random.randint(10,18)

    randJSON["is_free"] = True
    if (random.randint(0,1)):
        randJSON["is_free"] = False
    
    randJSON["developers"] = "Ryan and Evan"
    if (len(devs) and random.randint(0,2)):
        rand = random.randint(0,len(devs)-1)
        randJSON["developers"] = devs[rand]
    
    randJSON["publishers"] = "Ryan and Evan"
    if (len(pubs) and random.randint(0,2)):
        rand = random.randint(0,len(pubs)-1)
        randJSON["publishers"] = pubs[rand]

    rand1 = False
    rand2 = False
    rand3 = False
    if (random.randint(0,1)):
        rand1 = True
    if (random.randint(0,1)):
        rand2 = True
    if (random.randint(0,1)):
        rand3 = True

    randJSON["platforms"] = {"windows": rand1, "mac": rand2, "linux": rand3}
    
    temp_cats = []
    if len(cats):
        for x in range(0, random.randint(1,len(cats))):
            temp_cats.append({"id": x, "description": cats[random.randint(0,len(cats)-1)]})
    randJSON["cats"] = temp_cats

    temp_genres = []
    if len(genres):
        for x in range(0, random.randint(1,len(genres))):
            temp_genres.append({"id": x, "description": cats[random.randint(0,len(genres)-1)]})
    randJSON["genres"] = temp_genres

    randJSON["screenshot_count"] = random.randint(0,10)

    randJSON["movie_count"] = random.randint(0,5)

    randJSON["coming_soon"] = False
    
    randJSON["release_date"] = "May 4, 2019"

    randJSON["score_rank"] = []

    # The reviews don't really matter since this is random
    randJSON["positive"] = random.randint(0,100) * random.randint(0,100)
    randJSON["negative"] = random.randint(0,100) * random.randint(0,100)
    randJSON["userscore"] = 0
    randJSON["owners"] = "20,000,000 .. 50,000,000"
    if (random.randint(0,1)):
        randJSON["owners"] = "20,000,000 .. 50,000,000"
    if (random.randint(0,2)):
        randJSON["owners"] = "0 .. 20,000,000"

    rand = random.randint(0,2000)
    randJSON["avg_play_forever"] = rand + random.randint(0,100)
    randJSON["avg_play_2weeks"] = rand + random.randint(0,100)
    randJSON["median_play_forever"] = rand + random.randint(0,100)
    randJSON["median_play_2weeks"] = rand + random.randint(0,100)

    randJSON["price"] = 0
    randJSON["initialprice"] = 0
    if(not randJSON["is_free"]):
        rand = (random.randint(0,80)*100)-1
        randJSON["price"] = rand
        randJSON["initialprice"] = rand + (random.randint(0,50)*5)

    randJSON["discount"] = randJSON["initialprice"] + randJSON["price"]

    randJSON["supported_languages"] = langs[random.randint(0,len(langs)-1)]

    randJSON["ccu"] = math.floor(math.log10(random.randint(1,10000))) * random.randint(1,1000) + random.randint(1,100)

    #print( tags[random.randint(0,len(tags)-1)] )
    randJSON["tags"]= {}
    if len(tags):
        for x in range(0, random.randint(0,20)):
            randJSON["tags"][tags[random.randint(0,len(tags)-1)]] = random.randint(0,1000)

    return randJSON



#retrieve list of all possible platforms, categories, genres, languages, and tags for vectorization
def getPlatforms(games):
    platforms = []
    for game in games.values():
        game_platforms = game.get_platforms()
        if game_platforms != None and len(game_platforms) != 0:
            for platform in game_platforms:
                if (not platform in platforms):
                    platforms.append(platform)
    return platforms

def getDevelopers(games, mini = 1):
    developers = []
    occ = defaultdict(int) #number of occurences
    for game in games.values():
        game_developers = game.get_developers()
        if game_developers != None and len(game_developers) != 0:
            for developer in game_developers:
                occ[developer] += 1
                if (occ[developer] >= mini) and (not developer in developers):
                    developers.append(developer)
    return developers

def getPublishers(games, mini = 1):
    publishers = []
    occ = defaultdict(int) #number of occurences
    for game in games.values():
        game_publishers = game.get_publishers()
        if game_publishers != None and len(game_publishers) != 0:
            for publisher in game_publishers:
                occ[publisher] += 1
                if (occ[publisher] >= mini) and (not publisher in publishers):
                    publishers.append(publisher)
    return publishers

def getCategories(games):
    categories = []
    val = None
    for game in games.values():
        game_categories = game.get_categories()
        if game_categories != None and len(game_categories) != 0:
            for category in game_categories:
                val = category["description"]
                if not val in categories:
                    categories.append(val)
    return categories

def getGenres(games):
    genres = []
    val = None
    for game in games.values():
        game_genres = game.get_genres()
        if game_genres != None and len(game_genres) != 0:
            for genre in game_genres:
                val = genre["description"]
                if not val in genres:
                    genres.append(val)
    return genres

def getLanguages(games):
    langs = []
    for game in games.values():
        game_langs = game.get_supported_languages()
        if game_langs != None and len(game_langs) != 0:
            for lang in game_langs: #.split(", "):
                if not lang in langs:
                    langs.append(lang)
    return langs

#returns 
def getTags(games, mini = 100):
    tags = []
    occ = defaultdict(int) #number of occurences
    for game in games.values():
        game_tags = game.get_tags()
        if game_tags != None and len(game_tags) != 0:
            for key in game_tags.keys():
                occ[key] += 1
                if (occ[key] >= mini)  and (not key in tags):
                    tags.append(key)
    return tags

# returns a list of games that game out up to a variable number of years ago.
def getRecentGames(games, cutoff_year):
    old_games = []
    strdate = ""
    for game in games.values():
        splitdate = game.get_release_date().split(" ")
        if len(splitdate) == 3:
            strdate = splitdate[2]  
        if strdate.isdigit():
            curdate = int(strdate)
        else:
            curdate = 0
        if not ((game.get_positive() + game.get_negative()) > 0) and (game.get_release_date() != None) and (curdate >= cutoff_year):
            old_games.append(game.get_id())

    # construct recent game
    for game in old_games:
        games.pop(game)
    return games

def getRelevantGames(games, review_min):
    old_games = []
    for key, game in games.items():
        if (game.get_reviews() < review_min):
            old_games.append(key)

    # construct recent game
    for key in old_games:
        games.pop(key)
    return games

