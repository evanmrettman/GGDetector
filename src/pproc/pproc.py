from objects.app_entry import Game

def CreateGames(json_dicts):
    apps = []
    for d in json_dicts:
        inner_d = d[d.keys()[0]]
        if inner_d["success"] == True:
            if inner_d["data"]["type"] == "game":
                apps.append(Game(d))
    return apps