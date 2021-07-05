import pandas as pd 
import numpy as np
from sklearn.tree import DecisionTreeClassifier

url='https://drive.google.com/file/d/16FPLxyH77mp69Do1WB2PLzlWUNB-VPiq/view?usp=sharing'
file_id=url.split('/')[-2]
dwn_url='https://drive.google.com/uc?id=' + file_id

golf_df = pd.read_csv(dwn_url)

golf_df.columns=['outlook', 'temprature', 'humidity', 'windy', 'play']

golf_df = golf_df.apply(lambda x: x.astype(str).str.lower())

X = pd.get_dummies(golf_df[['outlook', 'temprature', 'humidity', 'windy']])
y = golf_df['play']

model = DecisionTreeClassifier()
model_train = model.fit(X, y)

def predict_playing_golf(a):
  predict = model_train.predict([a])
  if predict[0] == 'yes':
    return 1
  else:
    return 0