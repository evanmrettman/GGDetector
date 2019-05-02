from objects.game import Game
import utility.logging as log
from collections import defaultdict

def CreateGames(json_dicts):
    games = defaultdict(Game)
    for i, steam_response in enumerate(json_dicts):
        appid = list(steam_response.keys())[0]
        inner_d = steam_response[appid]
        if inner_d["success"] == True:
            if inner_d["data"]["type"] == "game":
                games[int(appid)] = Game(steam_response)
        log.sofar("Creating Games",i,len(json_dicts),10)
    return games

def ProcessAddSteamSpy(json_dicts, games):
    log.processing("Adding steam spy data...")
    for i, game in enumerate(games):
        game.addSteamSpyData(json_dicts)
        log.sofar("Adding steam spy data", i, len(json_dicts),10)