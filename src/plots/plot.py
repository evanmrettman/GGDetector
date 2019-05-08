import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter
from os import listdir
import files.parse as parse 
import pproc.pproc as pp

green = '#42f471'
red = '#f44141'

def createClassifierGraphs(fp_out,fp_in):

    global green
    global red

    for f in listdir(fp_in):
        percent = f[-7:-5]
        f = "%s%s" % (fp_in,f)
        percent_data = parse.readCSV(f)

        knn = []
        dtree = []
        rforest = []
        nbayes = []
        nnetwork = []
        svm = []

        for row in percent_data:
            name = row[0]
            if name == "KNN":
                knn.append(row[1:])
            elif name == "DTree":
                dtree.append(row[1:])
            elif name == "RForest":
                rforest.append(row[1:])
            elif name == "NBayes": # ignore nbayes because it sucks
                pass#nbayes.append(row[1:])
            elif name == "NNetwork":
                nnetwork.append(row[1:])
            elif name == "SVM":
                svm.append(row[1:])

        plotBoxplot("Classifiers with >%s%% Approved" % percent,
            "Classifiers",
            "Accuraccy",
            [
                "KNN",
                "DTree",
                "RForest",
                #"NBayes",
                "NNetwork",
                "SVM"
            ],
            [
                [float(r[0])*100 for r in knn],
                [float(r[0])*100 for r in dtree],
                [float(r[0])*100 for r in rforest],
                #[float(r[0])*100 for r in nbayes],
                [float(r[0])*100 for r in nnetwork],
                [float(r[0])*100 for r in svm],
            ],
            fp_out,
            red,
            green)

def plotBoxplot(name,xlabel,ylabel,catagories,data,fp,c_min,c_max):
    gray = '#a8a8a8'
    shortPhrase = ""
    limit = 10
    fig = plt.figure()

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.xticks(rotation=45)
    
    boxplot=plt.boxplot(data,labels=catagories)
    #plt.ylim([0,100])
    fig.suptitle("Boxplot of %s%s" % (name,shortPhrase))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, pos: str(y) + r'$\%$' if matplotlib.rcParams['text.usetex'] else str(y) + '%'))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    fig.savefig("%s/boxplot_%s.png" % (fp,str.lower(name).replace(" ","_").replace(">","")))
    #fig.gcf()

def createRandomGameGraphs(fp_in,fp_out, plats, cats, devs, pubs, genres, langs, tags):
    classified_games = parse.readCSV("%s/classified_games.csv" % fp_in)
    
    positive = defaultdict(int)
    negative = defaultdict(int)

    for game_data in classified_games:
        appid = game_data[0][5:]
        if appid.isdigit():
            appid = int(appid)
            if game_data[1] == "True":
                positive[appid] = pp.inputGame(pp.generateRandomGame(plats, cats, devs, pubs, genres, langs, tags, seed=appid))
            else:
                negative[appid] = pp.inputGame(pp.generateRandomGame(plats, cats, devs, pubs, genres, langs, tags, seed=appid))

    createGameGraphs(fp_out,positive,name="Successful")
    createGameGraphs(fp_out,negative,name="Unsuccessful")

def createGameGraphs(fp,games_dict, name=None):

    global green
    global red

    types = defaultdict(int)
    ages = defaultdict(int)
    free = defaultdict(int)
    developers = defaultdict(int)
    publishers = defaultdict(int)
    platforms = defaultdict(int)
    catagories = defaultdict(int)
    languages = defaultdict(int)
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
        for lang in game.get_supported_languages():
            languages[lang] += 1
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


    #plotHistogram("App Types","Percent","App Count",types,fp)
    plotHistogram("Ages" if name == None else ("Ages [%s]" % name),"What is the age requirement for games with age limits?",ages,fp,red,green)
    plotHistogram("Free Status" if name == None else ("Free Status [%s]" % name),"Is the game free?",free,fp,green,red)
    plotHistogram("Genres" if name == None else ("Genres [%s]" % name),"What are the top genres of games?",genres,fp,red,green)
    plotHistogram("Developers" if name == None else ("Developers [%s]" % name),"Who are the top developers?",developers,fp,red,green)
    plotHistogram("Publishers" if name == None else ("Publishers [%s]" % name),"Who are the top publishers?",publishers,fp,red,green)
    plotHistogram("Platforms" if name == None else ("Platforms [%s]" % name),"Whare are the supported operating systems?",platforms,fp,red,green)
    if len(catagories) > 0:
        plotHistogram("Catagories" if name == None else ("Catagories [%s]" % name),"What catagories does the game have?",catagories,fp,red,green)
    if len(release) > 0:
        plotHistogram("Release Date" if name == None else ("Release Date [%s]" % name),"When was the game released?",release,fp,red,green)
    if len(languages) > 0:
        plotHistogram("Languages" if name == None else ("Languages [%s]" % name),"When was the game released?",languages,fp,red,green)
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

    plt.xticks(rotation=45)

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
    #fig.gcf()
    plt.close('all')