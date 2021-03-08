# https://github.com/YouHoo0521/kaggle-march-madness-men-2019/blob/master/notebooks/models/KNN.ipynb

from tabulate import tabulate
import pandas as pd
import numpy as np
from sklearn import neighbors
from sklearn.metrics import log_loss
import MakeDataset
pd.set_option('display.max_columns', 500)

data = MakeDataset.get_boxscore_dataset_v1(2015)
print(tabulate(data.head(), headers="keys"))

cols = data.columns
diffCols = [s for s in cols if "mean" in s]
diffCats = []
for col in diffCols:
    cat = col.split('_')[0]
    if cat not in diffCats:
        diffCats.append(cat)

diffDict = {}
for team in [1, 2]:
    for cat in diffCats:
        diffDict[cat + '_diff_' + str(team)] = data[cat + '_team_mean' + str(team)] - data[
            cat + '_opp_mean' + str(team)]
        data.drop(columns=[cat + '_team_mean' + str(team),
                           cat + '_team_std' + str(team),
                           cat + '_opp_mean' + str(team),
                           cat + '_opp_std' + str(team)],
                  inplace=True)
# print(diffDict)
dfDiff = pd.DataFrame(diffDict, columns=diffDict.keys())
# dfDiff.head()
data.drop(columns=['season', 'daynum', 'numot', 'score1', 'score2', 'loc', 'seed1', 'seednum1', 'seed2', 'seednum2',
                   'confabbrev1', 'conf_descr1', 'confabbrev2', 'conf_descr2', 'teamname1', 'firstd1season1',
                   'lastd1season1', 'teamname2', 'firstd1season2', 'lastd1season2', 'seeddiff', 'ID'], inplace=True)

data = pd.concat([data, dfDiff], axis=1)
print(tabulate(data.head(), headers="keys"))

def inverse1and0(v):
    if (v == 1):
        return 0
    else:
        return 1

duplicateData = data.copy()
duplicateData['team1win']=duplicateData['team1win'].map(inverse1and0)
columns = list(duplicateData)

swapped = []
for col in columns:
    if col in swapped:
        continue
    if col.endswith('1'):
        col2 = col[:-1] + '2'
        col1idx = columns.index(col)
        col2idx = columns.index(col2)
        columns[col1idx], columns[col2idx] = columns[col2idx], columns[col1idx]
        swapped.append(col)

duplicateData.columns = columns
print(tabulate(duplicateData.head(), headers="keys"))

tourneyData = data.loc[data['tourney'] == 1]
data = pd.concat([data, duplicateData], sort=False)
regSeasonData = data.loc[data['tourney'] == 0]
regSeasonData.drop(columns = ['tourney'], inplace = True)
tourneyData.drop(columns = ['tourney'], inplace = True)

xtrain = np.array(regSeasonData.drop(columns = ['team1win', 'team1', 'team2']))
ytrain = np.array(regSeasonData['team1win'])
xtest = np.array(tourneyData.drop(columns = ['team1win', 'team1', 'team2']))
ytest = np.array(tourneyData['team1win'])

clf = neighbors.KNeighborsClassifier()
clf.fit(xtrain, ytrain)
testprobs = clf.predict_proba(xtest)
print(testprobs)

accuracy = clf.score(xtest, ytest)
test_loss = log_loss(ytest,testprobs[:, 0])
print(test_loss)
print(accuracy)