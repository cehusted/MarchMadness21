import warnings
warnings.simplefilter(action='ignore')
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

from getKenPom import getKPommy
from prepare_data import getTrainData
from test_data import getTestData


def balance_data(data, name):
    print("Balancing Data in {}...".format(name))
    before_counts = data['HomeTeamWon'].value_counts()
    if len(before_counts) == 2:
        (num_1s, num_0s) = list(before_counts)
    else:
        num_1s = len(data['HomeTeamWon'])
        num_0s = 0

    print(" -- Value counts before: [{}, {}]".format(num_0s, num_1s))
    numToBalance = (num_1s - num_0s) // 2
    team1 = data[data['HomeTeamWon'] == 1].sample(numToBalance).sort_index()
    team1['HomeTeamWon'] = 0
    col = team1.columns
    for column in col:
        if column[-2:] == "_1":
            team1.rename(columns={column: column.split('_')[0] + '_tmp'}, inplace=True)
        elif column[-2:] == "_2":
            team1.rename(columns={column: column.split('_')[0] + '_1'}, inplace=True)
            team1.rename(columns={column.split('_')[0] + '_tmp': column.split('_')[0] + '_2'}, inplace=True)

    assert(set(col) == set(team1.columns))
    data.loc[team1.index] = team1

    print(" -- Value counts after: {}".format(list(data['HomeTeamWon'].value_counts())))

    return data


def LogLoss(pred, GT):
    pred = pred.clip(0.000000001, 0.999999999)
    GT = GT.clip(0.000000001, 0.999999999)
    loss = -np.mean((GT * np.log(pred)) + (1 - GT) * np.log(1 - pred))
    return np.round(loss, 3)


KenPom = getKPommy()
gameData = getTrainData()
testData = getTestData()

'''
All Features Available:
                ['TourneyGame', 'AvgScore_1', 'AvgOppScore_1', 'AvgFG_1', 'AvgOppFG_1', 'AvgFG3_1', 'AvgOppFG3_1',
                 'AvgFT_1', 'AvgOppFT_1', 'TOmargin_1', 'PointMargin_1', 'WinsTop25_1', 'WinsTop5_1', 'rank_1',
                 'seed_1', 'wins_1', 'losses_1', 'wpct_1', 'adjem_1', 'adjo_1', 'adjd_1', 'adjt_1',
                 'luck_1', 'adjems_1', 'oppos_1', 'oppds_1', 'adjemn_1', 'AvgScore_2', 'AvgOppScore_2', 'AvgFG_2',
                 'AvgOppFG_2','AvgFG3_2', 'AvgOppFG3_2', 'AvgFT_2', 'AvgOppFT_2', 'TOmargin_2', 'PointMargin_2',
                 'WinsTop25_2', 'WinsTop5_2', 'rank_2', 'seed_2', 'wins_2', 'losses_2', 'wpct_2',
                 'adjem_2', 'adjo_2', 'adjd_2', 'adjt_2', 'luck_2', 'adjems_2', 'oppos_2', 'oppds_2', 'adjemn_2',]'''

featuresToUse = ['TourneyGame', 'AvgScore_1', 'AvgFG_1', 'AvgFG3_1', 'AvgFT_1', 'TOmargin_1', 'WinsTop25_1',
                 'WinsTop5_1', 'rank_1', 'seed_1', 'wpct_1', 'adjem_1', 'adjo_1', 'adjd_1', 'luck_1', 'oppos_1',
                 'AvgScore_2', 'AvgFG_2', 'AvgFG3_2', 'AvgFT_2', 'TOmargin_2', 'WinsTop25_2', 'WinsTop5_2', 'rank_2',
                 'seed_2', 'wpct_2', 'adjem_2', 'adjo_2', 'adjd_2', 'luck_2', 'oppos_2']

valData = gameData[gameData['TourneyGame'] == 1]
trainData = gameData[gameData['TourneyGame'] == 0]
valData = balance_data(valData, 'valData')
trainData = balance_data(trainData, 'trainData')

print("Splitting into train/val/test sets...")
trainY = trainData.pop('HomeTeamWon').astype('int')
trainX = trainData[featuresToUse]
valY = valData.pop('HomeTeamWon').astype('int')
valX = valData[featuresToUse]
testX = testData[featuresToUse]

assert(list(valX.columns) == list(trainX.columns))

trainScaler = StandardScaler().fit(trainX)
trainX = pd.DataFrame(trainScaler.transform(trainX), index=trainX.index, columns=trainX.columns)
valX = pd.DataFrame(trainScaler.transform(valX), index=valX.index, columns=valX.columns)

########### Neural Network Parameters #############
hidden_layer_sizes = (10, 6, 4)
activation = 'relu'
solver = 'adam'
alpha = 0.0001
batch_size = 32
learning_rate = 'constant'
learning_rate_init = 0.01
max_iter = 100
random_state = 69
tol = 0.0001
verbose = False
###################################################

for alpha in [0.0001, 0.001, 0.01, 0.1]:
    for learning_rate_init in [0.0001, 0.001, 0.01, 0.1]:
        for tol in [0.0001, 0.001, 0.01]:
            for batch_size in [32, 64, 128]:
                NN = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, alpha=alpha,
                                   batch_size=batch_size, learning_rate=learning_rate, learning_rate_init=learning_rate_init,
                                   max_iter=max_iter, random_state=random_state, tol=tol, verbose=verbose)

                NN_trained = NN.fit(trainX, trainY)
                preds = NN.predict_proba(valX)
                print("({}, {}, {}, {}) --- Train Loss: {} --- Test Loss: {}".format(alpha, learning_rate_init, tol,
                      batch_size, np.round(NN_trained.best_loss_, 3), LogLoss(preds[:, 1], valY)))
