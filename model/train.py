import numpy as np                                # For matrix operations and numerical processing
import pandas as pd                               # For munging tabular data
from time import gmtime, strftime                 # For labeling SageMaker models, endpoints, etc.
import sys                                        # For writing outputs to notebook
import math                                       # For ceiling function
import json                                       # For parsing hosting outputs
import os                                         # For manipulating filepath names
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, accuracy_score,confusion_matrix 
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve

data = pd.read_csv('./bank-additional/bank-additional-full.csv')
data['no_previous_contact'] = np.where(data['pdays'] == 999, 1, 0)                                 # Indicator variable to capture when pdays takes a value of 999
data['not_working'] = np.where(np.in1d(data['job'], ['student', 'retired', 'unemployed']), 1, 0)   # Indicator for individuals not actively employed
model_data = pd.get_dummies(data)                                                                  # Convert categorical variables to sets of indicators
model_data = model_data.drop(['duration', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed'], axis=1)

train_data, test_data = np.split(model_data.sample(frac=1, random_state=1729), [int(0.75 * len(model_data))])  

train_data = pd.concat([train_data['y_yes'], train_data.drop(['y_no', 'y_yes'], axis=1)], axis=1)
train_data.to_csv('train.csv', index=False, header=False)

test_data = pd.concat([test_data['y_yes'], test_data.drop(['y_no', 'y_yes'], axis=1)], axis=1)
test_data = test_data.drop(['y_yes'],axis=1)
test_data.to_csv('test_data_1.csv', index=False, header=False)

y_train = train_data['y_yes'].values
x_train = train_data.drop(labels=['y_yes'],axis=1, inplace=False)

kfold = StratifiedKFold(n_splits=3)
random_state = 10

RFC = RandomForestClassifier()

## Search grid for optimal parameters
rf_param_grid = {"max_depth":[5] ,
              "max_features":[15] ,
              "n_estimators" :[200],
              "min_samples_leaf":[11],
              "min_samples_split":[100],
              "criterion": ["gini"]}

gsRFC = GridSearchCV(RFC,param_grid = rf_param_grid, cv=kfold, scoring="roc_auc", n_jobs= 4, verbose = 1)

gsRFC.fit(x_train,y_train)

RFC_best = gsRFC.best_estimator_
gsRFC.best_params_, gsRFC.best_score_
joblib.dump(gsRFC, "model.joblib")
print('Model training completed..')