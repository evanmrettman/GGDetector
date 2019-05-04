from collections import defaultdict
import utility.logging as log

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

    __vector = []

    def __initHelp(self,d,key,default_value):
        return d[key] if key in d.keys() else default_value
        # improve this to have a better default value other than None
        # x = lambda key, default_value : __initHelp(d,index,default_value)

    # given a dictionary of a sucessful json request and it is a game, parse it as game object
    def __init__(self, steam_response):

        data = steam_response[list(steam_response.keys())[0]]["data"]

        self.__id = self.__initHelp(data,"steam_appid", self.__id)
        self.__type = self.__initHelp(data,"type", self.__type)
        self.__name = self.__initHelp(data,"name", self.__name)
        self.__required_age = self.__initHelp(data,"required_age", self.__required_age)
        self.__is_free = self.__initHelp(data,"is_free", self.__is_free)
        #self.__supported_languages = self.__initHelp(data,"supported_languages") # This may have to be parsed against a list of known languages (steamspy just lists this though)
        self.__developers = self.__initHelp(data,"developers", self.__developers)
        self.__publishers = self.__initHelp(data,"publishers", self.__publishers)
        self.__platforms = self.__initHelp(data,"platforms", self.__platforms) # windows, mac, linux
        self.__categories = self.__initHelp(data,"categories", self.__categories) # [id, descriptions]
        self.__genres = self.__initHelp(data,"genres", self.__genres) # [id, description]

        ss = self.__initHelp(data,"screenshots", self.__screenshot_count)
        self.__screenshot_count = len(ss) if ss != self.__screenshot_count else 0
        mo = self.__initHelp(data,"movies", self.__movie_count)
        self.__movie_count = len(mo) if mo != self.__movie_count else 0
        
        # coming_soon, date
        date = self.__initHelp(data,"release_date", defaultdict(str)) # not sure about this line
        self.__coming_soon = self.__initHelp(date,"coming_soon", self.__coming_soon)
        self.__release_date = self.__initHelp(date,"date", self.__release_date) 

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
        self.__score_rank = self.__initHelp(spy_response,"score_rank", self.__score_rank)
        self.__positive = self.__initHelp(spy_response,"positive", self.__positive)
        self.__negative = self.__initHelp(spy_response,"negative", self.__negative)
        self.__userscore = self.__initHelp(spy_response,"userscore", self.__userscore)
        self.__owners = self.__initHelp(spy_response,"owners", self.__owners)
        self.__avg_play_forever = self.__initHelp(spy_response,"average_forever", self.__avg_play_forever)
        self.__avg_play_2weeks = self.__initHelp(spy_response,"average_2weeks", self.__avg_play_2weeks)
        self.__median_play_forever = self.__initHelp(spy_response,"median_forever", self.__median_play_forever)
        self.__median_play_2weeks = self.__initHelp(spy_response,"median_2weeks", self.__median_play_2weeks)
        self.__price = self.__initHelp(spy_response,"price", self.__price)
        self.__initialprice = self.__initHelp(spy_response,"initialprice", self.__initialprice )
        self.__discount = self.__initHelp(spy_response,"discount", self.__discount)
        langstr = self.__initHelp(spy_response,"languages", self.__supported_languages)
        if langstr != None:
            self.__supported_languages = langstr.split(", ")
        self.__ccu = self.__initHelp(spy_response,"ccu", self.__ccu)
        self.__tags = self.__initHelp(spy_response,"tags" , self.__tags)
        

    def get_class(self): # TODO: make this more clear. temporary for now
        return self.__positive > self.__negative if self.__positive != None and self.__negative != None else False

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

    def get_score_rank(self):
        return self.__score_rank

    def get_positive(self):
        return self.__positive

    def get_negative(self):
        return self.__negative

    def get_userscore(self):
        return self.__userscore

    def get_owners(self):
        return self.__owners

    def get_avg_play_forever(self):
        return self.__avg_play_forever

    def get_avg_play_2weeks(self):
        return self.__avg_play_2weeks

    def get_median_play_forever(self):
        return self.__median_play_forever

    def get_median_play_2weeks(self):
        return self.__median_play_2weeks

    def get_price(self):
        return self.__price

    def get_initialprice(self):
        return self.__initialprice

    def get_discount(self):
        return self.__discount

    def get_supported_languages(self):
        return self.__supported_languages

    def get_ccu(self):
        return self.__ccu

    def get_tags(self):
        return self.__tags


    # pass a list of all possible platforms, categories, genres, languages, and tags to this function
    def vectorize(self, plats, cats, devs, pubs, genres, langs, tags):

        if not len(self.__vector) == 0:
            return self.__vector

        # FINISH THIS BY FINISHING PPROC TO GET LISTS OF COMPONENTS
        vector = []
        #vector.append(self.__id)
        #vector.append(self.__type)
        #vector.append(self.__name)
        vector.append(self.__required_age) # good?
        #vector.append(self.__is_free) # changing this
        if self.__is_free:
            vector.append(1)
        else:
            vector.append(0)
        

        #vector.append(self.__developers) # changing this
        for dev in devs:
            if dev in self.__developers:
                vector.append(1)
                #log.info("DEBUG: FOUND A MATCH")
            else:
                vector.append(0)

        #vector.append(self.__publishers) # changing this
        for pub in pubs:
            if pub in self.__publishers:
                vector.append(1)
            else:
                vector.append(0)

        # vector.append(self.__platforms) # changing this
        for plat in plats:
            if plat in self.__platforms:
                vector.append(1)
            else:
                vector.append(0)

        # vector.append(self.__categories) # changing this
        for cat in cats:
            if cat in self.__categories:
                vector.append(1)
            else:
                vector.append(0)

        # vector.append(self.__genres)
        for genre in genres:
            if genre in self.__genres:
                vector.append(1)
            else:
                vector.append(0)

        vector.append(self.__screenshot_count) # good?

        vector.append(self.__movie_count) # good?

        # The following 6 commented out vector components are meant for achieving other data elsewhere
        #vector.append(self.__coming_soon)
        #vector.append(self.__release_date)
        #vector.append(self.__score_rank)
        #vector.append(self.__positive) 
        #vector.append(self.__negative)
        #vector.append(self.__userscore)

        #vector.append(self.__owners) # changing
        vector.append(int.from_bytes(str.encode(self.__owners),'big')) #test this?

        vector.append(self.__avg_play_forever) # good?
        vector.append(self.__avg_play_2weeks) # good?
        vector.append(self.__median_play_forever) # good?
        vector.append(self.__median_play_2weeks) # good?
        vector.append(self.__price) # good?
        vector.append(self.__initialprice) # good?
        vector.append(self.__discount) # good?

        #vector.append(self.__supported_languages) # changing
        if(self.__supported_languages != None):
            for lang in self.__supported_languages:
                if lang in langs:
                    #log.info("DEBUG: lang match found")
                    vector.append(1)
                else:
                    vector.append(0)
        
        vector.append(self.__ccu) # good?

        #vector.append(self.__tags) # changing
        for tag in tags:
            if tag in self.__tags:
                vector.append(self.__tags[tag])
            else:
                vector.append(0)


        return vector

    def string(self):
        return "%10d : %s" % (self.__id,self.__name)