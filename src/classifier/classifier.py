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
from sklearn.model_selection import train_test_split

def getRandomInt():
    return random.randint(0,sys.maxsize)

def testClassifiers(fp,games,TestKNN=True,TestDTree=True,TestRForest=True,TestNBayes=True,TestNNetwork=True,TestSVM=True):

    fullpath = "%s/classifier_test.csv" % fp
    kf = KFold(n_splits=10)
    classifiers = []
    game_data = []
    game_classes = []

    for game in games.values():
        game_data.append(game.get_vector())
        game_classes.append(game.get_class())

    X_train,X_test,y_train,y_test = train_test_split(np.array(game_data).astype('float64'),np.asarray(game_classes).astype('float64'),test_size=0.33)

    log.info("Training Data: %dx%d" % (X_train.shape[0],X_train.shape[1]))
    log.info("Training Class Data: %d" % (y_train.shape[0]))
    log.info("Testing Data: %dx%d" % (X_test.shape[0],X_test.shape[1]))
    log.info("Testing Class Data: %d" % (y_test.shape[0]))

    knn_ks = range(1,21,4)
    random_range = range(0,1)
    tree_depth = [10,20,30,40,50,60,70,80,90,100,None]
    rforest_estimators = range(10,100,10)
    dict_to_parse = defaultdict(list)
    acc_data = []

    if TestKNN:
        log.info("\tTesting KNNs")
        for k in knn_ks:
            for weight in ["uniform","distance"]:
                for alg in ["ball_tree","kd_tree","brute"]:
                    c = KNeighborsClassifier(n_neighbors=k,weights=weight,algorithm=alg)
                    c.fit(X_train,y_train)
                    acc = accuracy_score(y_test,c.predict(X_test))
                    parse.appendCSV(fullpath,[["KNN",acc,k,weight,alg]])
                    log.info("\t\tAccuraccy %f with %d,%s,%s" % (acc,k,weight,alg))
        log.info("\tFinished KNNs")
    if TestDTree:
        log.info("\tTesting DTrees")
        for criteria in ["gini","entropy"]:
            for split in ["best","random"]:
                for depth in tree_depth:
                    for _ in random_range:
                        random_state = getRandomInt()
                        c = DecisionTreeClassifier(criterion=criteria,splitter=split,max_depth=depth,random_state=random_state)
                        c.fit(X_train,y_train)
                        acc = accuracy_score(y_test,c.predict(X_test))
                        parse.appendCSV(fullpath,[["DTree",acc,criteria,split,depth,random_state]])
                        log.info("\t\tAccuraccy %f with %s,%s,%s" % (acc,criteria,split,depth))
        log.info("\tFinished DTrees")
    if TestRForest:
        log.info("\tTesting RForests")
        for estimator in rforest_estimators:
            for criteria in ["gini","entropy"]:
                for depth in tree_depth:
                    for _ in random_range:
                        random_state = getRandomInt()
                        c = RandomForestClassifier(n_estimators=estimator,criterion=criteria,max_depth=depth,random_state=random_state)
                        c.fit(X_train,y_train)
                        acc = accuracy_score(y_test,c.predict(X_test))
                        log.info("\t\tAccuraccy %f with %s,%s,%s" % (acc,criteria,estimator,depth))
                        parse.appendCSV(fullpath,[["RForest",acc,estimator,criteria,depth,random_state]])
        log.info("\tFinished RForests")
    if TestNBayes:
        log.info("\tTesting NBayes")
        c = GaussianNB() # nothing to change that I understand
        c.fit(X_train,y_train)
        acc = accuracy_score(y_test,c.predict(X_test))
        log.info("\t\tAccuraccy %f" % (acc))
        parse.appendCSV(fullpath,[["NBayes",acc]])
        log.info("\tFinished NBayes")
    if TestNNetwork:
        log.info("\tTesting NNetworks")
        for active in ["identity","logistic","tanh","relu"]:
            for solve in ["lbfgs","sgd","adam"]:
                for _ in random_range:
                    random_state = getRandomInt()
                    c = MLPClassifier(activation=active,solver=solve,random_state=random_state)
                    c.fit(X_train,y_train)
                    acc = accuracy_score(y_test,c.predict(X_test))
                    log.info("\t\tAccuraccy %f with %s,%s" % (acc,active,solve))
                    parse.appendCSV(fullpath,[["NNetwork",acc,active,solve,random_state]])
        log.info("\tFinished NNetworks")
    if TestSVM:
        log.info("\tTesting SVMs")
        for kern in ["rbf","poly","sigmoid"]: # linear was real slow
            for _ in random_range:
                random_state = getRandomInt()
                c = SVC(gamma="scale",kernel=kern,random_state=random_state)
                c.fit(X_train,y_train)
                acc = accuracy_score(y_test,c.predict(X_test))
                log.info("\t\tAccuraccy %f with %s" % (acc,kern))
                parse.appendCSV(fullpath,[["SVM",acc,kern,random_state]])
        log.info("\tFinished SVMs")

if __name__ == "__main__":
    number_of_items = 100
    size_of_vector = 50
    number_of_classes = 2
    testClassifiers("Testing","",np.random.rand(number_of_items,size_of_vector).tolist(),np.random.randint(number_of_classes,size=number_of_items).tolist())