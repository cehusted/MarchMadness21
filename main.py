import warnings
warnings.simplefilter(action='ignore')
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

from getKenPom import getKPommy
from prepare_data import getTrainData
from test_data import getTestData
from simulateBracket import simulate


def buildModel(data):
    model = Sequential()
    model.add(Dense(32, input_shape=(len(data.columns),), activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dropout(0.05))
    model.add(Dense(2, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.0025), metrics=['accuracy'])

    return model

def hyperparameterSearch(hyperparameter_search):
    if hyperparameter_search:
        for hidden in [(16, 8, 4), (25, 25, 25, 25, 25), (256, 32, 8), (256, 128, 64, 32)]:
            for alpha in [0.0001, 0.001, 0.01]:
                for learning_rate_init in [0.0001, 0.001, 0.01]:
                    NN = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver,
                                       alpha=alpha,
                                       batch_size=batch_size, learning_rate=learning_rate,
                                       learning_rate_init=learning_rate_init,
                                       max_iter=max_iter, random_state=random_state, tol=tol, verbose=verbose)

                    NN_trained = NN.fit(trainX, trainY)
                    preds = NN.predict_proba(valX)
                    print("({}, {}, {}) --- Train Loss: {} --- Test Loss: {}".format(hidden, alpha, learning_rate_init,
                                                                                     np.round(NN_trained.best_loss_, 3),
                                                                                     LogLoss(preds[:, 1], valY)))

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

def predKeras(trainX, trainY, testX, b, i):
    model = buildModel(trainX)
    model.fit(trainX, trainY, batch_size=b, epochs=i, validation_split=0.05, shuffle=True, verbose=2, callbacks=[earlyStopping, adaptiveLR])
    return model.predict(testX, batch_size=b)

def predMLP(trainX, trainY):
    NN = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, alpha=alpha,
                       batch_size=batch_size, learning_rate=learning_rate, learning_rate_init=learning_rate_init,
                       max_iter=max_iter, random_state=random_state, tol=tol, verbose=verbose).fit(trainX, trainY)
    print("Best loss on MLP: {}".format(NN.best_loss_))
    return NN.predict_proba(testX)

KenPom = getKPommy()
gameData = getTrainData()
testData = getTestData()

'''
All Features Available:
                ['AvgScore_1', 'AvgOppScore_1', 'AvgFG_1', 'AvgOppFG_1', 'AvgFG3_1', 'AvgOppFG3_1',
                 'AvgFT_1', 'AvgOppFT_1', 'TOmargin_1', 'PointMargin_1', 'WinsTop25_1', 'WinsTop5_1', 'rank_1',
                 'seed_1', 'wins_1', 'losses_1', 'wpct_1', 'adjem_1', 'adjo_1', 'adjd_1', 'adjt_1',
                 'luck_1', 'adjems_1', 'oppos_1', 'oppds_1', 'adjemn_1', 'AvgScore_2', 'AvgOppScore_2', 'AvgFG_2',
                 'AvgOppFG_2','AvgFG3_2', 'AvgOppFG3_2', 'AvgFT_2', 'AvgOppFT_2', 'TOmargin_2', 'PointMargin_2',
                 'WinsTop25_2', 'WinsTop5_2', 'rank_2', 'seed_2', 'wins_2', 'losses_2', 'wpct_2',
                 'adjem_2', 'adjo_2', 'adjd_2', 'adjt_2', 'luck_2', 'adjems_2', 'oppos_2', 'oppds_2', 'adjemn_2']'''

featuresToUse = ['AvgScore_1', 'AvgOppScore_1', 'AvgFG_1', 'AvgOppFG_1', 'AvgFG3_1', 'AvgOppFG3_1',
                 'AvgFT_1', 'AvgOppFT_1', 'TOmargin_1', 'PointMargin_1', 'WinsTop25_1', 'WinsTop5_1',
                 'seed_1', 'wpct_1', 'adjo_1', 'adjd_1', 'luck_1', 'AvgScore_2', 'AvgOppScore_2', 'AvgFG_2',
                 'AvgOppFG_2','AvgFG3_2', 'AvgOppFG3_2', 'AvgFT_2', 'AvgOppFT_2', 'TOmargin_2', 'PointMargin_2',
                 'WinsTop25_2', 'WinsTop5_2', 'seed_2', 'wpct_2', 'adjo_2', 'adjd_2', 'luck_2']

# Split into train/val splits for practice training (on known tourney results), and balance team1 and team2 winning
valData = gameData[gameData['TourneyGame'] == 1]
trainData = gameData[gameData['TourneyGame'] == 0]
valData = balance_data(valData, 'valData')
trainData = balance_data(trainData, 'trainData')

# Separate ground truth from data
print("Splitting into train/val/test sets...")
trainY = to_categorical(np.array(trainData.pop('HomeTeamWon').astype('int')))
trainX = trainData[featuresToUse]
valY = to_categorical(np.array(valData.pop('HomeTeamWon').astype('int')))
valX = valData[featuresToUse]

assert(list(valX.columns) == list(trainX.columns))

# Center data (zero-mean) and reduce variance with Scaler
trainScaler = StandardScaler().fit(trainX)
trainX = pd.DataFrame(trainScaler.transform(trainX), index=trainX.index, columns=trainX.columns)
valX = pd.DataFrame(trainScaler.transform(valX), index=valX.index, columns=valX.columns)

################## MLP Parameters ##################
# Use these for hyperparameter tuning (grid search)
hidden_layer_sizes = (16, 8, 4)
activation = 'relu'
solver = 'adam'
alpha = 0.001
batch_size = 64
learning_rate = 'adaptive'
learning_rate_init = 0.001
max_iter = 100
random_state = 69
tol = 0.001
verbose = True
hyperparameter_search = False
###################################################
hyperparameterSearch(hyperparameter_search)

# Prepare callbacks and practice training on Keras model
earlyStopping = EarlyStopping(monitor="val_loss", patience=10, verbose=0, restore_best_weights=True)
adaptiveLR = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, verbose=1)
# model = buildModel(trainX)
# model.fit(trainX, trainY, batch_size=64, epochs=100, validation_data=(valX, valY), shuffle=True, verbose=2, callbacks=[earlyStopping, adaptiveLR])
# predsAll = model.predict(valX, batch_size=64)
# print("LogLoss on validation set: {}".format(LogLoss(predsAll[:, 1], np.argmax(valY, axis=1))))

# Prepare actual train/test data
testX = testData[featuresToUse]
gameData = balance_data(gameData, 'gameData')
trainY = gameData.pop('HomeTeamWon').astype('int')
trainX = gameData[featuresToUse]

# Center data (zero-mean) and reduce variance with Scaler
scaler = StandardScaler().fit(trainX)
trainX = pd.DataFrame(scaler.transform(trainX), index=trainX.index, columns=trainX.columns)
testX = testData[featuresToUse]
testX = pd.DataFrame(scaler.transform(testX), index=testX.index, columns=testX.columns)

# Run predictions on Keras model and sklearn-MLP model
preds_Keras = predKeras(trainX, to_categorical(np.array(trainY)), testX, batch_size, max_iter)
preds_MLP = predMLP(trainX, trainY)

# Prepare and save Stage2 submission file
preds_submission = testData.merge(pd.DataFrame(preds_Keras), left_index=True, right_index=True)
preds_submission.loc[preds_submission['TeamID_1'] < preds_submission['TeamID_2'], 'Pred'] = preds_submission[1]
preds_submission.loc[preds_submission['TeamID_1'] > preds_submission['TeamID_2'], 'Pred'] = preds_submission[0]
preds_submission = preds_submission[['ID', 'Pred']]
preds_submission['Pred'] = preds_submission['Pred'].clip(lower=0.05, upper=0.95)

print("Final predictions:", preds_submission)
preds_submission.to_csv("Stage2_Submission.csv", index=False)

print("Simulating bracket...")
winner = simulate(preds_submission)
print("\n --- {} is your predicted winner! ---".format(winner))