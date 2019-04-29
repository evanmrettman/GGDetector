from objects.app_entry import Game
import utility.logging as log

def CreateGames(json_dicts):
    apps = []
    for d in json_dicts:
        log.info(d)
        #inner_d = d[d.keys()[0]]
        inner_d = list(d.keys())[0]
        log.info(inner_d["success"])
        if inner_d["success"] == True:
            if inner_d["data"]["type"] == "game":
                apps.append(Game(d))
    return apps