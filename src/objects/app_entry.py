class Game:

    _id = 0
    _type = ""
    _name = ""
    _required_age = 0
    _is_free = False
    _supported_languages = "" # This may have to be parsed against a list of known languages
    _developers = []
    _publishers = []
    _platforms = [] # windows, mac, linux
    _categories = [] # [id, descriptions]
    _genres = [] # [id, description]
    _screenshot_count = 0
    _movie_count = 0
    _release_date = [] # coming_soon, date

    def __initHelp(self,d,key):
        return d[key] if key in d.keys() else None

    # given a dictionary of a sucessful json request and it is a game, parse it as game object
    def __init__(self, game_dict):
        data = game_dict[game_dict.keys()[0]]["data"]

        

        self._id = self.__initHelp(data,"steamapp_id")
        self._type = data["type"]
        self._name = data["name"]
        self._required_age = data["required_age"]
        self._is_free = data["is_free"]
        self._supported_languages = data["supported_languages"] # This may have to be parsed against a list of known languages
        self._developers = data["developers"]
        self._publishers = data["publishers"]
        self._platforms = data["platforms"] # windows, mac, linux
        self._categories = data["categories"] # [id, descriptions]
        self._genres = data["genres"] # [id, description]

        ss = self.__initHelp(data,"screenshots")
        self._screenshot_count = len(ss) if ss != None else 0
        self._movie_count = 0
        
        self._release_date = data["release_date"] # coming_soon, date
        

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

    def get_release_date(self):
        return self._release_date

    def string(self):
        return "%s" % (self._name)