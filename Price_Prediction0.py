from datetime import datetime
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM,Dense,Dropout

import pandas as pd

from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler



#load data
data = pd.read_csv("D:/Programing/FinalYear/Book1.csv")
data['Date'] = pd.to_datetime(data['Date'])
training_data = data
Dates_train = training_data['Date']
#print(data)
town = str(input("Enter town name : "))
    #getting a location to train
training_data = training_data.loc[training_data['Location'] == town]
test_data=training_data.loc[training_data['Date']>='2021-01-15']
test_data=test_data[['Date','Maize_White']]
# print('Training : ', training_data)
#normalizining the data to a range of 0 and 1

scaler=MinMaxScaler(feature_range=(0,1))
training_data=training_data[list(training_data )[2:8]]

training_data_scaled=scaler.fit_transform(training_data)

def Rnn():
    trainX = []  # training series
    trainY = []  # prediction series
    # months to predict
    months_predict=6
    # number of past months we want to base our prediction on
    months_past=12
    for i in range(months_past,len(training_data_scaled)-months_predict+1):
        trainX.append(training_data_scaled[i-months_past:i,0:training_data.shape[1]])
        trainY.append((training_data_scaled[i+months_predict-1:i+months_predict,0]))
    trainX,trainY=np.array(trainX),np.array(trainY)

#modelling a sequence of layers stack together

    model = Sequential()

#adding a layer1 to the model with batchsize=,numberofsteps=12,features=4
    model.add(LSTM(units=50,activation='relu',input_shape=(trainX.shape[1],trainX.shape[2]),return_sequences=True))
    #20% of the layers dropped out to avoid overfitting
    model.add(Dropout(0.2))
    model.add(LSTM(units=50,activation='relu',return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=1)) #output
    model.compile(optimizer = 'adam',loss='mse')
    model.fit(trainX,trainY,batch_size=32,epochs=30)


   # forecast_12=6#number of months predicted
    period_forecast=pd.date_range(list(Dates_train)[0],periods=months_predict,freq='1m').tolist()
    forecast=model.predict(trainX[-months_predict:])
   # print(forecast)
    forecast_copies=np.repeat(forecast,training_data.shape[1],axis=-1)
    pred_months=scaler.inverse_transform(forecast_copies)[:,0]
   # print('pre : [',pred_months,']')
    forecast_dates=[]
    for time_i in period_forecast:
        forecast_dates.append(time_i.date())
    df_forecast=pd.DataFrame({'Date':np.array(forecast_dates),'Maize_White':pred_months})
   # df_forecast.to_csv(f"D:/Programing/FinalYear/Price_Prediction/maize_white/{town}",index=False)
    results=pd.DataFrame({'Date ':np.array(forecast_dates),'ActualPrice':test_data['Maize_White'],'Predicted':pred_months})
    print('Periods :',df_forecast)
    print(results)

Rnn()
