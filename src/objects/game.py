from collections import defaultdict

class Game:

    # 14 vector components from steam api
    __id = 0
    __type = ""
    __name = ""
    __required_age = 0
    __is_free = False
    __developers = []
    __publishers = []
    __platforms = [] # windows, mac, linux
    __categories = [] # [id, descriptions]
    __genres = [] # [id, description]
    __screenshot_count = 0
    __movie_count = 0
    __coming_soon = False
    __release_date = ""
    
    #15 vector components from steam spy
    __score_rank = []
    __positive = 0
    __negative = 0
    __userscore = 0
    __owners = ""
    __avg_play_forever = 0
    __avg_play_2weeks = 0
    __median_play_forever = 0
    __median_play_2weeks = 0
    __price = 0
    __initialprice = 0
    __discount = 0
    __supported_languages = []
    __ccu = 0
    __tags = {}

    def __initHelp(self,d,key):
        return d[key] if key in d.keys() else None

    # given a dictionary of a sucessful json request and it is a game, parse it as game object
    def __init__(self, steam_response):

        data = steam_response[list(steam_response.keys())[0]]["data"]

        self.__id = self.__initHelp(data,"steam_appid")
        self.__type = self.__initHelp(data,"type")
        self.__name = self.__initHelp(data,"name")
        self.__required_age = self.__initHelp(data,"required_age")
        self.__is_free = self.__initHelp(data,"is_free")
        #self.__supported_languages = self.__initHelp(data,"supported_languages") # This may have to be parsed against a list of known languages (steamspy just lists this though)
        self.__developers = self.__initHelp(data,"developers")
        self.__publishers = self.__initHelp(data,"publishers")
        self.__platforms = self.__initHelp(data,"platforms") # windows, mac, linux
        self.__categories = self.__initHelp(data,"categories") # [id, descriptions]
        self.__genres = self.__initHelp(data,"genres") # [id, description]

        ss = self.__initHelp(data,"screenshots")
        self.__screenshot_count = len(ss) if ss != None else 0
        mo = self.__initHelp(data,"movies")
        self.__movie_count = len(mo) if mo != None else 0
        
        # coming_soon, date
        date = self.__initHelp(data,"release_date")
        self.__coming_soon = self.__initHelp(date,"coming_soon")
        self.__release_date = self.__initHelp(date,"date") 

        #default values for steam spy data, call addSteamSpyData after initialization
        self.__score_rank = []
        self.__positive = 0
        self.__negative = 0
        self.__userscore = 0
        self.__owners = ""
        self.__avg_play_forever = 0
        self.__avg_play_2weeks = 0
        self.__median_play_forever = 0
        self.__median_play_2weeks = 0
        self.__price = 0
        self.__initialprice = 0
        self.__discount = 0
        self.__supported_languages = []
        self.__ccu = 0
        self.__tags = defaultdict(int)

    def addSteamSpyData(self, spy_response):
        self.__score_rank = self.__initHelp(spy_response,"score_rank")
        self.__positive = self.__initHelp(spy_response,"positive")
        self.__negative = self.__initHelp(spy_response,"negative")
        self.__userscore = self.__initHelp(spy_response,"userscore")
        self.__owners = self.__initHelp(spy_response,"owners")
        self.__avg_play_forever = self.__initHelp(spy_response,"average_forever")
        self.__avg_play_2weeks = self.__initHelp(spy_response,"average_2weeks")
        self.__median_play_forever = self.__initHelp(spy_response,"median_forever")
        self.__median_play_2weeks = self.__initHelp(spy_response,"median_2weeks")
        self.__price = self.__initHelp(spy_response,"price")
        self.__initialprice = self.__initHelp(spy_response,"initialprice")
        self.__discount = self.__initHelp(spy_response,"discount")
        self.__supported_languages = self.__initHelp(spy_response,"languages")
        self.__ccu = self.__initHelp(spy_response,"ccu")
        self.__tags = self.__initHelp(spy_response,"tags")
        

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_required_age(self):
        return self.__required_age

    def get_is_free(self):
        return self.__is_free 

    def get_supported_languages(self):
        return self.__supported_languages 

    def get_developers(self):
        return self.__developers 

    def get_publishers(self):
        return self.__publishers 

    def get_platforms(self):
        return self.__platforms 

    def get_categories(self):
        return self.__categories 

    def get_genres(self):
        return self.__genres 

    def get_screenshot_count(self):
        return self.__screenshot_count 

    def get_movie_count(self):
        return self.__movie_count 

    def get_coming_soon(self):
        return self.__coming_soon

    def get_release_date(self):
        return self.__release_date

    def vectorize(self):
        vector = []
        #vector.append(self.__id)
        vector.append(self.__type)
        #vector.append(self.__name)
        vector.append(self.__required_age)
        vector.append(self.__is_free)
        vector.append(self.__developers)
        vector.append(self.__publishers)
        vector.append(self.__platforms)
        vector.append(self.__categories)
        vector.append(self.__genres)
        vector.append(self.__screenshot_count)
        vector.append(self.__movie_count)
        #vector.append(self.__coming_soon)
        #vector.append(self.__release_date)
        vector.append(self.__score_rank)
        vector.append(self.__positive)
        vector.append(self.__negative)
        vector.append(self.__userscore)
        vector.append(self.__owners)
        vector.append(self.__avg_play_forever)
        vector.append(self.__avg_play_2weeks)
        vector.append(self.__median_play_forever)
        vector.append(self.__median_play_2weeks)
        vector.append(self.__price)
        vector.append(self.__initialprice)
        vector.append(self.__discount)
        vector.append(self.__supported_languages)
        vector.append(self.__ccu)
        vector.append(self.__tags)

        return vector

    def string(self):
        return "%10d : %s" % (self.__id,self.__name)