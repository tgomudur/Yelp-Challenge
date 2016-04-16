
# coding: utf-8

# In[11]:

# All imports go here

import numpy as np
from numpy import genfromtxt
import csv
from sklearn import linear_model
from sklearn import preprocessing

from sklearn.metrics import mean_squared_error
from math import sqrt
# In[ ]:

def getRoundedThreshold(a, MinClip=0.5):
    return np.round(np.array(a, dtype=float) / MinClip) * MinClip

# Step 1 : Loading the User x Restaurant matrix.
#Y = np.transpose(genfromtxt('user_restr_mat_csv.csv', delimiter=','))
Y = genfromtxt('user_restr_matrix.csv', delimiter=',')

"""
# Using CSV module to load instead of genfromtxt

user_restr_arr = []
with open('user_restr_mat_csv.csv','r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        user_restr_arr.append(row)

Y = np.transpose(np.asarray(user_restr_arr))
"""
# Checking shape of Y
print "Shape of Y:"
print Y.shape


# In[6]:

# Step 2 : Loading the Restaurant feature matrix

X = genfromtxt('restr_feature_matrix.csv', delimiter=',')
print X.shape

x, y = int(Y.shape[0]), int(Y.shape[1])
r = np.zeros(Y.shape)
r[:] = Y[:]
dt = np.random.randint(1, size=(x, y))
va = np.random.randint(1, size=(x, y))
count = 0
idx = []
actual = []
print "Running"
for i in range(0, x):
    for j in range(0, y):
        if r[i, j] != 0:
            count += 1
            if count%5 == 0:
		idx.append([i, j])
		actual.append(Y[i,j])
		Y[i,j] = 0

print "Done"

# Filling missing places with mean
for i in range(X.shape[1]):
    tmp = X[:,i][X[:,i] != -1]
    feature_mean = sum(tmp)/len(tmp)
    X[:,i][X[:,i] == -1] = feature_mean
# In[ ]:
user_params = []
model = linear_model.SGDRegressor()
for i in range(int(Y.shape[0])):
    model.fit(X[0], Y[i])
    user_params.append(np.asarray(model.coef_))
    
user_params =  np.asarray(user_params)
print "Printing user params for user 0"
print user_params[0]

#predicted_ratings = user_params.dot(X.T)

minmaxscaler = preprocessing.MinMaxScaler(feature_range=(0, 5), copy=True)
#scaled_ratings =  minmaxscaler.fit_transform(predicted_ratings)
scaled_params = []
for i in range(len(user_params)):
    temp = user_params[i]
    temp = np.array(temp).reshape((len(temp), 1))
    scaled_params.append(minmaxscaler.fit_transform(temp).reshape(len(user_params[i],)))
scaled_params = np.asarray(scaled_params)
#scaled_params = minmaxscaler.fit_transform(user_params)
predicted_ratings= scaled_params.dot(X.T)

#print "Scaled_params"
#print scaled_params[0]
#predicted_ratings = scaled_params.dot(X.T)

print "Predicted ratings"
print predicted_ratings
#print predicted_ratings
#print "Scaled ratings"
#print scaled_ratings
scaled_ratings = []

for i in range(len(predicted_ratings)):
    temp = predicted_ratings[i]
    temp = np.array(temp).reshape((len(temp), 1))
    scaled_ratings.append(minmaxscaler.fit_transform(temp).reshape(len(predicted_ratings[i],)))
#scaled_ratings = minmaxscaler.fit_transform(predicted_ratings)
scaled_ratings = np.asarray(scaled_ratings)
rounded_ratings = getRoundedThreshold(scaled_ratings)
#predicted_ratings = getRoundedThreshold(predicted_ratings)
predicted = []
predicted2 = []
for i,j in idx:
    predicted2.append(rounded_ratings[i, j])
    predicted.append(scaled_ratings[i, j])
    #predicted.append(predicted_ratings[i, j])
print "Actual and Predicted"
print actual[:5]
print predicted[:5]
rms = sqrt(mean_squared_error(actual, predicted))
rms2 = sqrt(mean_squared_error(actual, predicted2))
print rms
print rms2
