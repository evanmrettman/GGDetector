import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

def createGameGraphs(fp,games_dict):

    types = defaultdict(int)
    ages = defaultdict(int)
    free = defaultdict(int)
    developers = defaultdict(int)
    publishers = defaultdict(int)
    platforms = defaultdict(int)
    catagories = defaultdict(int)
    genres = defaultdict(int)
    sscount = []
    mvcount = []
    release = defaultdict(int)

    for game in games_dict.values():
        types[game.get_type()] += 1
        if game.get_required_age() != None:
            if game.get_required_age() != 0:
                ages[str(game.get_required_age())] += 1
        else:
            ages["No Age Listed"] += 1
        free["Yes" if game.get_is_free() else "No"] += 1
        if game.get_developers() != None:
            for dev in game.get_developers():
                developers[dev] += 1
        else:
            developers["No Developer Listed"] += 1
        for pub in game.get_publishers():
            if pub != "":
                publishers[pub] += 1
            else:
                publishers["No Publisher Listed"] += 1
        for key, value in game.get_platforms().items():
            if value:
                platforms[key] += 1
        if game.get_categories() != None:
            for cata in game.get_categories():
                catagories[cata["description"]] += 1
        else:
            catagories["No Catagories Listed"] += 1
        if game.get_genres() != None:
            for genre in game.get_genres():
                genres[genre["description"]] += 1
        else:
            genres["No Genres Listed"] += 1
        sscount.append(game.get_screenshot_count())
        mvcount.append(game.get_movie_count())
        if game.get_release_date() != "" and str.isdigit(game.get_release_date()[-4:]):
            release[game.get_release_date()[-4:]] += 1
        elif game.get_coming_soon():
            release["Coming Soon"] += 1
        else: 
            release["No Release Info"] += 1

    green = '#42f471'
    red = '#f44141'

    #plotHistogram("App Types","Percent","App Count",types,fp)
    plotHistogram("Ages","What is the age requirement for games with age limits?",ages,fp,red,green)
    plotHistogram("Free Status","Is the game free?",free,fp,green,red)
    plotHistogram("Genres","What are the top genres of games?",genres,fp,red,green)
    plotHistogram("Developers","Who are the top developers?",developers,fp,red,green)
    plotHistogram("Publishers","Who are the top publishers?",publishers,fp,red,green)
    plotHistogram("Platforms","Whare are the supported operating systems?",platforms,fp,red,green)
    plotHistogram("Catagories","What catagories does the game have?",catagories,fp,red,green)
    plotHistogram("Release Date","When was the game released?",release,fp,red,green)
    if False:
        plt.show()

def plotHistogram(name,xlabel,d,fp,c_min,c_max):
    gray = '#a8a8a8'
    shortPhrase = ""
    dcopy = d.copy()
    limit = 10
    fig = plt.figure()

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    if len(d) > limit/2:
        plt.xticks(rotation=90)
        if len(d) > limit:
            shortPhrase = " (Limited to %d Catagories)" % limit
            dcopy = dict(Counter(dcopy).most_common(limit))    
    
    catagories = list(dcopy.keys())
    counts = [float(i)/sum(list(dcopy.values()))*100 for i in list(dcopy.values())]

    barlist=plt.bar(catagories,counts,color=gray)
    barlist[counts.index(min(counts))].set_color(c_min)
    barlist[counts.index(max(counts))].set_color(c_max)
    for bar in barlist:
        bar.set_edgecolor("black")
    #plt.ylim([0,100])
    fig.suptitle("Histogram of %s%s" % (name,shortPhrase))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, pos: str(y) + r'$\%$' if matplotlib.rcParams['text.usetex'] else str(y) + '%'))
    plt.xlabel(xlabel)
    #plt.ylabel(ylabel)
    plt.tight_layout()
    fig.savefig("%s/histogram_%s.png" % (fp,str.lower(name)))