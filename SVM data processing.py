import numpy as np
import pandas as pd
import sklearn
import sklearn.metrics as metrics
from sklearn import svm
import csv
from sklearn import preprocessing
import pickle

dataneg = pd.read_csv("Negative_samples_102_.csv")
datapos = pd.read_csv("Positive_samples_102_.csv")

training_data = [];

datan = np.array(dataneg);
datap = np.array(datapos[0:745]);


labeln = datan[:,15]
labelp = datap[0:745,15]


#print(type(labeln))

labels = np.append(labelp,labeln).astype(int)
#print(labels.shape)
#print(labels)

datan = datan[:,0:15];
datap = datap[:,0:15];

data = np.append(datan,datap,axis = 0)

#print(type(data))
#print(data.shape)
#print(data[0])

x = data
y = labels
#print(y)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)
print(x_train[0], y_train[0])

clf = svm.SVC(kernel = 'poly',degree = 5, C=100)
clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)
acc = metrics.accuracy_score(y_test,y_pred)

print(acc)

