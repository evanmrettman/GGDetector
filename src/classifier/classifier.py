import sys
import random
import datetime
import utility.logging as log
import files.parse as parse
from collections import defaultdict
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

def getRandomInt():
    return random.randint(0,sys.maxsize)

def testClassifiers(fp,games):

    kf = KFold(n_splits=10)
    classifiers = []
    game_data = []
    game_classes = []

    for game in games.values():
        game_data.append(game.get_vector())
        game_classes.append(game.get_class())

    X = np.array(game_data).astype('float64')
    y = np.asarray(game_classes).astype('float64')

    log.info("Data: %dx%d" % (X.shape[0],X.shape[1]))
    log.info("Classes: %d" % (y.shape[0]))

    TestKNN = False
    TestDTree = True
    TestRForest = True
    TestNBayes = True
    TestNNetwork = True
    TestSVM = True

    numKNN = 0
    numDTree = 0
    numRForest = 0
    numNBayes = 1
    numNNetwork = 0
    numSVM = 0

    # Create KNN
    if TestKNN:
        for k in range(1,21,4):
            for weight in ["uniform","distance"]:
                for alg in ["ball_tree","kd_tree","brute"]:
                    numKNN += 1
                    classifiers.append(KNeighborsClassifier(n_neighbors=k,weights=weight,algorithm=alg))

    # Create Decision Tree
    if TestDTree:
        for criteria in ["gini","entropy"]:
            for split in ["best","random"]:
                for depth in [10,20,30,40,50,60,70,80,90,100,None]:
                    #for _ in range(0,20):
                    numDTree += 1
                    state = getRandomInt()
                    classifiers.append(DecisionTreeClassifier(criterion=criteria,splitter=split,max_depth=depth,random_state=state))

    # Create Random Forest
    if TestRForest:
        for estimator in range(10,100,10):
            for criteria in ["gini","entropy"]:
                for depth in [10,20,30,40,50,60,70,80,90,100,None]:
                    #for _ in range(0,20):
                    numRForest += 1
                    state = getRandomInt()
                    classifiers.append(RandomForestClassifier(n_estimators=estimator,criterion=criteria,max_depth=depth,random_state=state))

    # Create Naive Bayes
    if TestNBayes:
        classifiers.append(GaussianNB()) # nothing to change that I understand

    # Create Neural Network
    if TestNNetwork:
        for active in ["identity","logistic","tanh","relu"]:
            for solve in ["lbfgs","sgd","adam"]:
                for rate in ["cosntant","invscaling","adaptive"]:
                    #for _ in range(0,20):
                    numNNetwork += 1
                    state = getRandomInt()
                    classifiers.append(MLPClassifier(activation=active,solver=solve,learning_rate=rate,random_state=state))
    
    # Create SVM
    if TestSVM:
        for kern in ["rbf","linear","poly","sigmoid","precomputed"]:
            for _ in range(0,20):
                numSVM += 1
                state = getRandomInt()
                classifiers.append(SVC(kernel=kern,random_state=state))

    now = datetime.datetime.now()
    filename = "%s/classifier_metrics_%s.csv" % (fp,"%d-%d-%d_%d-%d.%d_%d" % (now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond))

    log.info("Running tests on %d KNN, %d DTree, %d RForest, %d NBayes, %d NNetwork, and %d numSVM." % (numKNN,numDTree,numRForest,numNBayes,numNNetwork,numSVM))

    parse.createCSV(filename,[["Classifier Name","Accuracy Score"]])
    dict_to_parse = defaultdict(list)
    i = 0
    for classifier in classifiers:

        try:
            classifier.fit(X,y) # fit it
        except Exception as e:
            log.info(e)
            while True:
                pass

        class_name = ""
        if isinstance(classifier,KNeighborsClassifier):
            class_name = "KNN"
        elif isinstance(classifier,DecisionTreeClassifier):
            class_name = "Decision Tree"
        elif isinstance(classifier,RandomForestClassifier):
            class_name = "Random Forest"
        elif isinstance(classifier,GaussianNB):
            class_name = "Gaussian Naive Bayes"
        elif isinstance(classifier,MLPClassifier):
            class_name = "Multi-layered Neural Network"
        elif isinstance(classifier,SVC):
            class_name = "Support Vector Machine"

        class_list = dict_to_parse[class_name]
        acc = accuracy_score(y,classifier.predict(X))
        if len(class_list) == 0:
            dict_to_parse[class_name] = [0,0,0]
            class_list = dict_to_parse[class_name]
        class_list[0] += acc # summation of acc
        class_list[1] += 1 # incriment count
        class_list[2] = class_list[0] / class_list[1]
        i += 1
        log.sofar("Testing Classifiers @ %s" % class_name,i,len(classifiers),len(classifiers))

    list_to_append = []
    for key, value in dict_to_parse.items():
        list_to_append.append([key,value[2]])
    parse.appendCSV(filename,list_to_append)

if __name__ == "__main__":
    number_of_items = 100
    size_of_vector = 50
    number_of_classes = 2
    testClassifiers("Testing","",np.random.rand(number_of_items,size_of_vector).tolist(),np.random.randint(number_of_classes,size=number_of_items).tolist())