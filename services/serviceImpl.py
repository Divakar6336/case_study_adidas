import pandas as pd 
from fastapi.encoders import jsonable_encoder
import json 
import os 
import pickle 
import numpy as np 
import sklearn 
from sklearn.model_selection import train_test_split 
import lightgbm as lgb 
from sklearn.metrics import accuracy_score 

version =0 
os.makedirs('/home/usr/app/dao/models', exist_ok=True)
filename=f'/home/usr/app/dao/models/model_{version}.pkl'
#filename= f'/Users/divakarsharma/Downloads/Adidas-Case-study/codebase/model_{version}.pkl'
#logging.config.fileConfig(fname=os.path.join(os.getcwd(), 'config.conf'), disable_existing_loggers=False)

#logger = logging.getLogger('sLogger')

def missingvalue(df):
    cols=df.select_dtypes('object').columns
    cols=cols.tolist()
    df['HomePlanet'].fillna(df['HomePlanet'].value_counts().index[0],inplace=True)
    df['CryoSleep'].fillna(df['CryoSleep'].value_counts().index[0],inplace=True)
    df['Destination'].fillna(df['Destination'].value_counts().index[0],inplace=True)
    df['VIP'].fillna(df['VIP'].value_counts().index[0],inplace=True)
    cols1=df.select_dtypes('float64').columns
    cols1=cols1.tolist()
    for i in cols1:
        df[i]=df[i].fillna(df[i].mean())
    return df

def Onehotencoding(df1):
    df1=df1.join(pd.get_dummies(df1['HomePlanet'],prefix='HomePlanet',prefix_sep='_'))
    df1=df1.join(pd.get_dummies(df1['CryoSleep'],prefix='CryoSleep',prefix_sep='_'))
    df1=df1.join(pd.get_dummies(df1['Destination'],prefix='Destination',prefix_sep='_'))
    df1=df1.join(pd.get_dummies(df1['VIP'],prefix='VIP',prefix_sep='_'))
    df1.drop(['HomePlanet','CryoSleep','Destination','VIP'],axis=1,inplace=True)
    return df1

def pre_processing(df):
    df.drop(['PassengerId','Name','Cabin'],axis=1,inplace=True)
    df=missingvalue(df)
    cols=df.select_dtypes('object').columns.tolist()
    df=Onehotencoding(df)
    return df

def model_training(df):
	result = {}

	df1=pre_processing(df)
	y=df1['Transported']
	col=df1.columns
	col=col.delete(6)
	print(col)
	x=df1[col]
	print(len(df1.columns))

	x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=5,stratify = y,test_size = 0.40)
	clf=lgb.LGBMClassifier(max_bin=250,learning_rate=0.13,num_iterations=150,min_gain_to_split=0.3,max_depth=20)
	clf.fit(x_train,y_train)
	pickle.dump(clf, open(filename, 'wb'))
	result["Accuracy on train data"]=clf.score(x_train,y_train)
	result["Accuracy on test data"]=clf.score(x_test,y_test)

	return result

def model_prediction(request):

	jsonbody=jsonable_encoder(request)
	df= pd.DataFrame.from_dict([jsonbody])
	

	if jsonbody['HomePlanet'] == 'Earth':
		df['HomePlanet_Earth'] = 1
		df['HomePlanet_Europa'] = 0
		df['HomePlanet_Mars'] = 0

	if jsonbody['HomePlanet'] == 'Mars':
		df['HomePlanet_Earth']=0
		df['HomePlanet_Europa'] = 0
		df['HomePlanet_Mars'] = 1

	if jsonbody['HomePlanet'] =='Europa':
		df['HomePlanet_Earth']=0
		df['HomePlanet_Europa'] = 1
		df['HomePlanet_Mars'] = 0

	if jsonbody['CryoSleep']:
		df['CryoSleep_False'] = 0
		df['CryoSleep_True'] = 1
	else:
		df['CryoSleep_False'] = 1
		df['CryoSleep_True'] = 0

	if jsonbody['Destination'] == 'TRAPPIST-1e':
		df['Destination_55 Cancri e'] = 0
		df['Destination_PSO J318.5-22'] = 0
		df['Destination_TRAPPIST-1e'] = 1

	if jsonbody['Destination'] == '55 Cancri e':
		df['Destination_55 Cancri e'] = 1
		df['Destination_PSO J318.5-22'] = 0
		df['Destination_TRAPPIST-1e'] = 0 

	if jsonbody['Destination'] == 'PSO J318.5-22':
		df['Destination_55 Cancri e'] = 0
		df['Destination_PSO J318.5-22'] = 1
		df['Destination_TRAPPIST-1e'] = 0

	if jsonbody['VIP']:
		df['VIP_False']= 0
		df['VIP_True'] = 1
	else:
		df['VIP_False']= 1
		df['VIP_True'] = 0

	df.drop(['HomePlanet', 'CryoSleep', 'Destination', 'VIP'], axis=1, inplace=True)
	print(df.columns)
	model=pickle.load(open(filename, 'rb'))
	if model.predict(df)[0]:
		jsonbody['Transported'] = 'True'
	else:
		jsonbody['Transported'] = 'False'
	return jsonbody















