import numpy as np
import sklearn
import sklearn.metrics as metrics
from sklearn import svm
from sklearn import datasets
import pickle

with open('test_model','rb') as f:
    test_mod = pickle.load(f)

x,y = datasets.load_breast_cancer(return_X_y= True)

x2 = np.array([2.309e+01, 1.983e+01, 1.521e+02, 1.682e+03, 9.342e-02, 1.275e-01, 1.676e-01, 1.003e-01, 1.505e-01, 5.484e-02, 1.291e+00, 7.452e-01, 9.635e+00, 1.802e+02, 5.753e-03, 3.356e-02, 3.976e-02, 2.156e-02, 2.201e-02, 2.897e-03, 3.079e+01, 2.387e+01, 2.115e+02, 2.782e+03, 1.199e-01, 3.625e-01, 3.794e-01, 2.264e-01, 2.908e-01, 7.277e-02])
x3 = np.reshape(x2,(-1,30))
y_pred = test_mod.predict(x3)
print(y_pred)