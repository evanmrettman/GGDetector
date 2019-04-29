from collections import defaultdict

class Game:

    # 14 vector components from steam api
    _id = 0
    _type = ""
    _name = ""
    _required_age = 0
    _is_free = False
    _developers = []
    _publishers = []
    _platforms = [] # windows, mac, linux
    _categories = [] # [id, descriptions]
    _genres = [] # [id, description]
    _screenshot_count = 0
    _movie_count = 0
    _coming_soon = defaultdict(False)
    _release_date = defaultdict("")
    
    #15 vector components from steam spy
    _score_rank = []
    _positive = 0
    _negative = 0
    _userscore = 0
    _owners = ""
    _avg_play_forever = 0
    _avg_play_2weeks = 0
    _median_play_forever = 0
    _median_play_2weeks = 0
    _price = 0
    _initialprice = 0
    _discount = 0
    _supported_languages = []
    _ccu = 0
    _tags = defaultdict(0)

    def __initHelp(self,d,key):
        return d[key] if key in d.keys() else None

    # given a dictionary of a sucessful json request and it is a game, parse it as game object
    def __init__(self, steam_response):

        data = steam_response[list(steam_response.keys())[0]]["data"]

        self._id = self.__initHelp(data,"steam_appid")
        self._type = self.__initHelp(data,"type")
        self._name = self.__initHelp(data,"name")
        self._required_age = self.__initHelp(data,"required_age")
        self._is_free = self.__initHelp(data,"is_free")
        #self._supported_languages = self.__initHelp(data,"supported_languages") # This may have to be parsed against a list of known languages (steamspy just lists this though)
        self._developers = self.__initHelp(data,"developers")
        self._publishers = self.__initHelp(data,"publishers")
        self._platforms = self.__initHelp(data,"platforms") # windows, mac, linux
        self._categories = self.__initHelp(data,"categories") # [id, descriptions]
        self._genres = self.__initHelp(data,"genres") # [id, description]

        ss = self.__initHelp(data,"screenshots")
        self._screenshot_count = len(ss) if ss != None else 0
        mo = self.__initHelp(data,"movies")
        self._movie_count = len(mo) if mo != None else 0
        
        # coming_soon, date
        date = self.__initHelp(data,"release_date")
        self._coming_soon = self.__initHelp(date,"coming_soon")
        self._release_date = self.__initHelp(date,"date") 

    def addSteamSpyData(self, spy_response):
        self._score_rank = self.__initHelp(spy_response,"score_rank")
        self._positive = self.__initHelp(spy_response,"positive")
        self._negative = self.__initHelp(spy_response,"negative")
        self._userscore = self.__initHelp(spy_response,"userscore")
        self._owners = self.__initHelp(spy_response,"owners")
        self._avg_play_forever = self.__initHelp(spy_response,"average_forever")
        self._avg_play_2weeks = self.__initHelp(spy_response,"average_2weeks")
        self._median_play_forever = self.__initHelp(spy_response,"median_forever")
        self._median_play_2weeks = self.__initHelp(spy_response,"median_2weeks")
        self._price = self.__initHelp(spy_response,"price")
        self._initialprice = self.__initHelp(spy_response,"initialprice")
        self._discount = self.__initHelp(spy_response,"discount")
        self._supported_languages = self.__initHelp(spy_response,"languages")
        self._ccu = self.__initHelp(spy_response,"ccu")
        self._tags = self.__initHelp(spy_response,"tags")
        

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_required_age(self):
        return self._required_age

    def get_is_free(self):
        return self._is_free 

    def get_supported_languages(self):
        return self._supported_languages 

    def get_developers(self):
        return self._developers 

    def get_publishers(self):
        return self._publishers 

    def get_platforms(self):
        return self._platforms 

    def get_categories(self):
        return self._categories 

    def get_genres(self):
        return self._genres 

    def get_screenshot_count(self):
        return self._screenshot_count 

    def get_movie_count(self):
        return self._movie_count 

    def get_coming_soon(self):
        return self._coming_soon

    def get_release_date(self):
        return self._release_date

    def vectorize(self):
        vector = []
        vector.append(self._id)
        vector.append(self._type)
        vector.append(self._name)
        vector.append(self._required_age)
        vector.append(self._is_free)
        vector.append(self._developers)
        vector.append(self._publishers)
        vector.append(self._platforms)
        vector.append(self._categories)
        vector.append(self._genres)
        vector.append(self._screenshot_count)
        vector.append(self._movie_count)
        vector.append(self._coming_soon)
        vector.append(self._release_date)
        vector.append(self._score_rank)
        vector.append(self._positive)
        vector.append(self._negative)
        vector.append(self._userscore)
        vector.append(self._owners)
        vector.append(self._avg_play_forever)
        vector.append(self._avg_play_2weeks)
        vector.append(self._median_play_forever)
        vector.append(self._median_play_2weeks)
        vector.append(self._price)
        vector.append(self._initialprice)
        vector.append(self._discount)
        vector.append(self._supported_languages)
        vector.append(self._ccu)
        vector.append(self._tags)

    def string(self):
        return "%10d : %s" % (self._id,self._name)