import sys
import random
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

def testClassifiers(name,fp,data,classes):

    classifiers = []
    X = np.asarray(data)
    y = np.asarray(classes)

    # Create KFolds
    kf = KFold(n_splits=2)


    # Create KNN
    for k in range(1,21,2):
        for weight in ["uniform","distance"]:
            for alg in ["ball_tree","kd_tree","brute"]:
                classifiers.append(KNeighborsClassifier(n_neighbors=k,weights=weight,algorithm=alg,n_jobs=-1))

    # Create Decision Tree
    for criteria in ["gini","entropy"]:
        for split in ["best","random"]:
            for depth in [10,20,30,40,50,60,70,80,90,100,None]:
                for _ in range(0,20):
                    state = getRandomInt()
                    classifiers.append(DecisionTreeClassifier(criterion=criteria,splitter=split,max_depth=depth,random_state=state))

    # Create Random Forest
    for estimator in range(10,100,10):
        for criteria in ["gini","entropy"]:
            for depth in [10,20,30,40,50,60,70,80,90,100,None]:
                for _ in range(0,20):
                    state = getRandomInt()
                    classifiers.append(RandomForestClassifier(n_estimators=estimator,criterion=criteria,max_depth=depth,random_state=state))

    # Create Naive Bayes
    classifiers.append(GaussianNB()) # nothing to change that I understand

    # Create Neural Network
    for active in ["identity","logistic","tanh","relu"]:
        for solve in ["lbfgs","sgd","adam"]:
            for rate in ["cosntant","invscaling","adaptive"]:
                for _ in range(0,20):
                    state = getRandomInt()
                    classifiers.append(MLPClassifier(activation=active,solver=solve,learning_rate=rate,random_state=state))
    
    # Create SVM
    for kern in ["rbf","linear","poly","sigmoid","precomputed"]:
        for _ in range(0,20):
            state = getRandomInt()
            classifiers.append(SVC(kernel=kern,random_state=state))

    for train_indexs, test_indexs in kf.split(X):
        X_train, y_train, X_test, y_test = X[train_indexs], y[train_indexs], X[test_indexs], y[test_indexs]
        print(len(classifiers))
        break
        for classifier in classifiers:
            classifier.fit(X_train,y_train)
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
            print("%s Accuraccy: %.2f" % (class_name,accuracy_score(classifier.predict(X_test),y_test)))

if __name__ == "__main__":
    number_of_items = 100
    size_of_vector = 50
    number_of_classes = 2
    testClassifiers("Testing","",np.random.rand(number_of_items,size_of_vector).tolist(),np.random.randint(number_of_classes,size=number_of_items).tolist())