
# coding: utf-8

# In[37]:

import numpy as np

# X  = feature vector of all restaurants

X = np.asarray(
[[ 0.9, 0 ],
 [ 1, 0.01],
 [ 0.99 , 0],
 [ 0.1  , 1],
 [ 0   ,0.9]])

# Y = Each row is a vector of user ratings for all restaurants
# Y = rating of user j on restaurant i

Y = np.transpose(np.asarray([[5,5,0,0],[5,0,0,0],[0,4,0,0],[0,0,5,4],[0,0,5,0]]))

print X
print Y


# In[56]:

# Here Y[1] indicates second feature of the business.
user_params = []
for i in range(int(Y.shape[0])):
    model.fit(X, Y[i])
    user_params.append(np.asarray(model.coef_))
user_params =  np.asarray(user_params)


# In[60]:

# Finding the predicted ratings of user for a restaurant

# Each row is a vector of one user ratings for all restaurants
user_params.dot(X.T)


# In[72]:

# Scale ratings to 0-5

# max_rating = 5
# scaled_params = []
# for myarr in user_params:
#     scaled_params.append(myarr/float(np.amax(myarr))*max_rating)

# # user_params = (user_params/np.amax(user_params))*max_rating
# # user_params.dot(X.T)
# scaled_params = np.asarray(scaled_params)
# scaled_params
# scaled_params.dot(X.T)

# OUTPUT:
"""
Out[72]:
array([[ 4.5       ,  4.99876367,  4.95      ,  0.37636653, -0.11127012],
       [ 4.5       ,  4.99848786,  4.95      ,  0.3487856 , -0.13609296],
       [ 0.03620135,  0.09022372,  0.03982148,  5.00402237,  4.5       ],
       [ 0.26154263,  0.34060292,  0.28769689,  5.02906029,  4.5       ]])
"""


# In[81]:

# Scale rating 0-5 
from sklearn import preprocessing
"""
array([[ 4.5       ,  5.0000845 ,  4.95      ,  0.50845032,  0.00760529],
       [ 3.942307  ,  4.38034111,  4.3365377 ,  0.43803411,  0.        ],
       [ 0.        ,  0.05      ,  0.        ,  5.        ,  4.5       ],
       [ 0.07650202,  0.10661774,  0.08415222,  2.17004984,  1.94539465]])
"""
minmaxscaler = preprocessing.MinMaxScaler(feature_range=(0, 5), copy=True)

scaled_params = minmaxscaler.fit_transform(user_params)
predicted_ratings = scaled_params.dot(X.T)

print predicted_ratings


# In[79]:

# Lets try rounding to nearest 0.5

def getRoundedThreshold(a, MinClip=0.5):
    return np.round(np.array(a, dtype=float) / MinClip) * MinClip

predicted_ratings = getRoundedThreshold(predicted_ratings)

print predicted_ratings


# In[82]:

# Finding RMSE 

from sklearn.metrics import mean_squared_error
from math import sqrt

actual_ratings = np.transpose(np.asarray([[5,5,0,0],[5,5,0,0],[5,4,0,0],[0,0,5,4],[0,0,5,4]]))

rms = sqrt(mean_squared_error(actual_ratings, predicted_ratings))

print rms


# In[ ]:



