import pandas as pd
import numpy as np
from sklearn.metrics import log_loss
from sklearn.linear_model import LogisticRegression
import MakeDataset
from tabulate import tabulate

data = MakeDataset.get_train_data_v1(2015)

X_train = data.loc[data.tourney == 0, ['seeddiff']].dropna()
X_test = data.loc[data.tourney == 1, ['seeddiff']].dropna()
y_train = data.loc[X_train.index, 'team1win']
y_test = data.loc[X_test.index, 'team1win']
print(tabulate(X_train.head(), headers="keys"))

clf = LogisticRegression(penalty='l2', fit_intercept=False, C=0.0001, verbose=False, max_iter=1000, solver='lbfgs')
clf.fit(X_train, y_train)
pred_train = pd.DataFrame({'ID':data.loc[X_train.index, 'ID'], 'Pred':clf.predict_proba(X_train)[:, 0], 'Train':True})
pred_test = pd.DataFrame({'ID':data.loc[X_test.index, 'ID'], 'Pred':clf.predict_proba(X_test)[:, 0], 'Train':False})
pred = pd.concat([pred_train, pred_test])[['ID', 'Pred', 'Train']]
print(tabulate(pred.head(), headers="keys"))

train_loss = log_loss(y_train, pred.loc[pred.Train, 'Pred'])
test_loss = log_loss(y_test, pred.loc[~pred.Train, 'Pred'])
train_acc = np.mean(y_train == clf.predict(X_train))
test_acc = np.mean(y_test == clf.predict(X_test))
print('train accuracy:{:0.2f}\ttest accuracy:{:0.2f}'.format(train_acc, test_acc))
print('train log_loss:{:0.2f}\ttest log_loss:{:0.2f}'.format(train_loss, test_loss))