from collections import defaultdict
from objects.game import Game
import utility.logging as log

class Games:

    __training = {}

    __developers = []
    __publishers = []
    __platforms = []
    __catagories = []
    __genres = []
    __tags = []
    __languages = []

    def __createGameDict(self,steam_dict,spy_dict):
        games = defaultdict(Game)
        for i, steam_response in enumerate(steam_dict):
            appid = list(steam_response.keys())[0]
            inner_d = steam_response[appid]
            if inner_d["success"] == True:
                if inner_d["data"]["type"] == "game":
                    games[int(appid)] = Game(steam_response,spy_dict[appid])
            log.sofar("Creating Games",i,len(steam_dict),10)
        return games

    def __init__(self,steam_dict,spy_dict):
        self.__training = self.__createGameDict(steam_dict,spy_dict)
        
        for game in self.__training.values():
            pass
         

    def vectorize(self,testing_dict=None):
        testing = None
        if testing_dict != None:
            testing = defaultdict(Game)
            self.__createGameDict(testing_dict)
