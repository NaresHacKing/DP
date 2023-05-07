from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import csv

import re
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
training = pd.read_csv('E:\Project\DP\static/assets\Training.csv')
testing= pd.read_csv('E:\Project\DP\static/assets\Testing.csv')
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']
y1= y
reduced_data = training.groupby(training['prognosis']).max()
#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']  
testy    = le.transform(testy)
clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf, x_test, y_test, cv=3)
# print (scores)
#print(scores.mean())
model=SVC()
model.fit(x_train,y_train)
#print("for svm: ")
#print(model.score(x_test,y_test))
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols
severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()
symptoms_dict = {}
dic = {}


# Create your views here.

def index(request):
    
    return render(request, 'index.html')

def dis_list(request):
    file = open("E:\Project\DP\static/assets\Diseases.csv")
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row[1])
    file.close()

    if request.method == 'GET':
        check = request.GET.get('dis_value')
        print(check)
        context = {'dis_value': check}
        if check == 'yes':
            context['dis'] = rows
        else:
            context['dis'] = {}
    return JsonResponse(context)

def symptoms_list(request):
    file = open("E:\Project\DP\static/assets\Symptoms.csv")
    sym = csv.reader(file)
    rows = []
    for row in sym:
        rows.append(row[1])
    file.close()
    if request.method == 'GET':
        context = {
            'symptoms':rows,
            #'range':range(1, 365)
        }
    return JsonResponse(context)


def check_sym(request):
    if request.method =='GET' and 'days' and 'dis' in request.GET:
        selected_disease = request.GET.get('dis')
        print("disease: ", selected_disease)
        days = request.GET.get('days')
        print("days: ", days)
        #tree_to_code(clf, cols)
        tree_ = clf.tree_
        feature_name = [
        cols[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
        ]
        response = {}
        #chk_dis=",".join(feature_names).split(",")
        symptoms_present = []
        def recurse(node, depth):
            global symptoms_given
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]

                if name == selected_disease:
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = print_disease(tree_.value[node])
                print("Node: ", node, present_disease)
                # print( "You may have " +  present_disease )
                red_cols = reduced_data.columns
                symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
                # dis_list=list(symptoms_present)
                # if len(dis_list)!=0:
                #     print("symptoms present  " + str(list(symptoms_present)))
                # print("symptoms given "  +  str(list(symptoms_given)) )
                #print("Are you experiencing any ")
                print(symptoms_given)
                response['result']=list(symptoms_given)
            
        recurse(0,1)
    return JsonResponse({'result':list(symptoms_given)})

def check_disease(request):
    getSeverityDict()
    getDescription()
    getprecautionDict()
    #temp = loader.get_template("check_symptoms.html")
    file = open("E:\Project\DP\static/assets\Symptoms.csv")
    sym = csv.reader(file)
    rows = []
    for row in sym:
        rows.append(row[1])
    file.close()

    context = {
        'symptoms':rows,
        'range':range(1, 365)
    }

    if request.method =='GET' and 'list' in request.GET:
        print(request.GET.get('list'))
        selected_disease = request.GET.get('dis')
        print("disease: ", selected_disease)
        days = request.GET.get('days')
        print("days: ", days)
        check_dis = request.GET.get('list')
        print("check: ", check_dis)
        lst = check_dis.split(' ')
        print(lst)
        #tree_to_code(clf, cols)
        tree_ = clf.tree_
        feature_name = [
        cols[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
        ]

        #chk_dis=",".join(feature_names).split(",")
        symptoms_present = []
        def recurse(node, depth):
            global present_disease
            global second_prediction
            global description_list
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]

                if name == selected_disease:
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = print_disease(tree_.value[node])
                print("Node: ", node, present_disease)
                # print( "You may have " +  present_disease )

                second_prediction=sec_predict(lst)
                # print(second_prediction)
                calc_condition(lst,int(days))
                if(present_disease[0]==second_prediction[0]):
                    print("You may have ", present_disease[0])
                    print(description_list[present_disease[0]])
                    precution_list=precautionDictionary[present_disease[0]]
                    print("Take following measures : ")
                    for  i,j in enumerate(precution_list):
                        print(i+1,")",j)
                    return JsonResponse({'present': present_disease[0], 'desc': description_list[present_disease[0]]})

                else:
                    print("You may have ", present_disease[0], "or ", second_prediction[0])
                    print(description_list[present_disease[0]])
                    print(description_list[second_prediction[0]])
                    precution_list=precautionDictionary[present_disease[0]]
                    print("Take following measures : ")
                    for  i,j in enumerate(precution_list):
                        print(i+1,")",j)
                    return JsonResponse({'present': present_disease[0],'sec':second_prediction[0], 'desc1': description_list[present_disease[0]], 'desc2':description_list[second_prediction[0]]})


                # print(description_list[present_disease[0]])
                """precution_list=precautionDictionary[present_disease[0]]
                print("Take following measures : ")
                for  i,j in enumerate(precution_list):
                    print(i+1,")",j)"""
                
        recurse(0, 1)
        #return JsonResponse({'present': present_disease[0],'sec':second_prediction[0], 'desc1': description_list[present_disease[0]], 'desc2':description_list[second_prediction[0]]})
    #else: print('no response')
    return JsonResponse({'present': present_disease[0],'sec':second_prediction[0], 'desc1': description_list[present_disease[0]], 'desc2':description_list[second_prediction[0]]})


def sec_predict(symptoms_exp):
    df = pd.read_csv('E:\Project\DP\static/assets\Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])

def print_disease(node):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))

def calc_condition(exp,days):
    sum=0
    for item in exp:
         sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        print("You should take the consultation from doctor.")
        return 'You should take the consultation from doctor.'
    else:
        print("It might not be that bad but you should take precautions.")
        return 'It might not be that bad but you should take precautions.'


def getDescription():
    global description_list
    with open('E:\Project\DP\static/assets\symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)

def getSeverityDict():
    global severityDictionary
    with open('E:\Project\DP\static/assets\Symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass

def getprecautionDict():
    global precautionDictionary
    with open('E:\Project\DP\static/assets\symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)

