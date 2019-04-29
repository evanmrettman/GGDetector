class AppEntry:

    _id = 0
    _type = ""
    _name = ""
    _steam_appid = ""
    _required_age = 0
    _is_free = False
    _supported_languages = "" # This may have to be parsed against a list of known languages
    _developers = []
    _publishers = []
    _platforms = [False,False,False] # windows, mac, linux
    _categories = [] # [id, descriptions]
    _genres = [] # [id, description]
    _screenshot_count = 0
    _movie_count = 0
    _release_date = [] # coming_soon, date


    def __init__(self, app_id, type, app_name, steam_appid, required_age, is_free, supported_languages, developers, publishers, platforms, cateogries, genres, screenshot_count, movie_count, release_date):
        self._id = str(app_id)
        self._name = str(app_name)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type
    
    def get_steam_appid(self):
        return self._steam_appid

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