from collections import defaultdict
from objects.game import Game

class Games:

    __training = {}

    __developers = []
    __publishers = []
    __platforms = []
    __catagories = []
    __genres = []
    __tags = []
    __languages = []

    def __createGameDict(self,game_dict):
        games = defaultdict(Game)
        for i, steam_response in enumerate(game_dict):
            appid = list(steam_response.keys())[0]
            inner_d = steam_response[appid]
            if inner_d["success"] == True:
                if inner_d["data"]["type"] == "game":
                    games[int(appid)] = Game(steam_response)
            log.sofar("Creating Games",i,len(game_dict),10)
        return games

    def __init__(self,steam_dict,spy_dict):
        self.__training = self.__createGameDict(training_dict)
        
        for game in self.__training.values():

         

    def vectorize(self,testing_dict=None):
        testing = None
        if testing_dict != None:
            testing = defaultdict(Game)
            self.__createGameDict(testing_dict)
