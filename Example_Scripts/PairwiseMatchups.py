# https://github.com/YouHoo0521/kaggle-march-madness-men-2019/blob/master/notebooks/eda/pairwise_matchups.org

from fancyimpute import NuclearNormMinimization
from matplotlib import pyplot as plt
from tabulate import tabulate
import seaborn as sns
import pandas as pd
import numpy as np
import MakeDataset

data = MakeDataset.get_boxscore_dataset_v1(2015)
data['scorediff'] = data['score1'] - data['score2']                         # difference in scores
data['score_w'] = np.where(data.team1win == 1, data.score1, data.score2)    # winning and losing scores
data['score_l'] = np.where(data.team1win == 0, data.score1, data.score2)
print('Data size = {}'.format(data.shape))
print(tabulate(data.head(), headers="keys"))

TeamConferences = (pd.read_csv('DataFiles/MTeamConferences.csv').pipe(lambda x:x[x['Season'] == 2015]))
teams_ordered = list(TeamConferences.sort_values(['ConfAbbrev', 'TeamID'])['TeamID'])
teams_pairwise = [(t1, t2) for t1 in teams_ordered for t2 in teams_ordered]

n_missing = data.isna().sum().rename('n_missing')
print(tabulate(data.describe().append(n_missing), headers="keys"))

# This figure shows the pairwise matchups between teams. The teams are ordered by conference.
# The diagonal blocks indicate that teams play with [almost] every other team within their conference.
# The games across conferences are much more sparse.
pairwise_matchups = (data[data['tourney'] == 0]
					 .pipe(lambda x: x.groupby(['team1', 'team2'])['scorediff'].size() > 0)
					 .reindex(teams_pairwise).fillna(False))
pairwise_matchups.loc[pairwise_matchups[pairwise_matchups].swaplevel().index.values] = True
pairwise_matchups = pairwise_matchups.unstack()
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(pairwise_matchups.loc[teams_ordered, teams_ordered], ax=ax, cbar=False)
ax.set_title('Regular Season Pairwise Matchups')
plt.show()

tourney_pairwise_matchups = (data[data['tourney'] == 1]
							 .pipe(lambda x: x.groupby(['team1', 'team2'])['scorediff'].size() > 0)
							 .reindex(teams_pairwise).fillna(False))
tourney_pairwise_matchups.loc[tourney_pairwise_matchups[tourney_pairwise_matchups].swaplevel().index.values] = True
tourney_pairwise_matchups = tourney_pairwise_matchups.unstack()
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(tourney_pairwise_matchups.loc[teams_ordered, teams_ordered], ax=ax, cbar=False)
ax.set_title('Tourney Season Pairwise Matchups')
plt.show()

# Matrix completion using convex optimization to find low-rank solution that still matches observed values. Slow!
pairwise_scorediff = (data[data['tourney'] == 0]
                      .pipe(lambda x: x.groupby(['team1', 'team2'])['scorediff'].mean()).reindex(teams_pairwise))
has_values = ~pairwise_scorediff.isna()
pairwise_scorediff.loc[pairwise_scorediff[has_values].swaplevel().index.values] = (-pairwise_scorediff[has_values]).values
pairwise_scorediff = pairwise_scorediff.unstack()
X_filled_nnm = NuclearNormMinimization(verbose=True).fit_transform(pairwise_scorediff)

# Accuracy
df_pred = pd.DataFrame(X_filled_nnm, index=pairwise_scorediff.index, columns=pairwise_scorediff.columns)
tourney_matchups = data.loc[data['tourney'] == 1, ['team1', 'team2']]
y_pred = np.array([df_pred.loc[i, j] for i, j in tourney_matchups.values])
y_true = data.loc[data['tourney'] == 1, 'scorediff']
print('accuracy = {}'.format(np.mean((y_pred > 0) == (y_true > 0))))

# Prediction vs. Actual
fig, ax = plt.subplots(figsize=(10,10))
ax.scatter(y_true, y_pred)
ax.grid(True)
ax.plot(np.arange(-20, 20), np.arange(-20, 20))
ax.set_xlabel('actual')
ax.set_ylabel('pred')
plt.show()