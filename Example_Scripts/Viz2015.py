# https://github.com/YouHoo0521/kaggle-march-madness-men-2019/blob/master/notebooks/eda/eda_2015.org

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from tabulate import tabulate
import MakeDataset

data = MakeDataset.get_train_data_v1(season=2015)           # (7699, 29)

# difference in scores
data['scorediff'] = data['score1'] - data['score2']

# winning and losing scores
data['score_w'] = np.where(data.team1win == 1, data.score1, data.score2)
data['score_l'] = np.where(data.team1win == 0, data.score1, data.score2)
print('Data size = {}'.format(data.shape))
print(tabulate(data.head(), headers="keys"))

n_missing = data.isna().sum().rename('n_missing')
print(tabulate(data.describe().append(n_missing), headers="keys"))

# Distribution of points from each team
# An initial look at the distribution of points scored by team 1 (with lower ID) and team 2 (with higher ID).
# As expected, there’s nothing special here which means that team IDs are probably assigned arbitrarily.
fig, axes = plt.subplots(2, 2, figsize=(8, 8), sharex=True, sharey=True)
for i, (is_tourney, df) in enumerate(data.groupby('tourney')):
    color = '#1f77b4' if is_tourney == 0 else '#ff7f0e'
    axes[i,0].scatter(df.score1, df.score2, s=1, c=color)
    axes[i,1].hexbin(df.score1, df.score2, bins='log', gridsize=50)
    lims = [20, 125]
    axes[i,0].set_ylabel('Team 2 Score ({})'.format('Regular' if is_tourney == 0 else 'Tourney'))
    axes[i,1].set_xlim(lims)
    axes[i,1].set_ylim(lims)
    for j in range(2):
        axes[i,j].plot(lims, lims, c='r', lw=0.5)
axes[1,0].set_xlabel('Team 1 Score')
axes[1,1].set_xlabel('Team 1 Score')
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.05, hspace=0.05)
plt.suptitle('Bivariate Distribution of Points')
plt.show()

# This figure shows the result of the games between seeded teams.
# Win, loss, and difference in seeds are from the perspective of team 1, or the team with the lower ID. For example,
# there were 3 tournament games in which team 1 was the underdog by 15 seed points, and all resulted in a loss.
# There were also two upsets in the tournament in which teams who had 11 seed point advantage lost the game.
df_tmp = data.groupby(['tourney', 'seeddiff'])['team1win'].agg(['sum', 'size']).reset_index()
fig, axes = plt.subplots(2, 1, figsize = (7, 10), sharex=True)
for i, (is_tourney, df) in enumerate(df_tmp.groupby('tourney')):
    axes[i].bar(df.seeddiff, df['size'], label='Loss')
    axes[i].bar(df.seeddiff, df['sum'], label='Win')
    axes[i].set_title('Regular' if is_tourney == 0 else 'Tourney')
axes[1].set_xlabel('Difference in Seeds')
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='right')
plt.suptitle("Proportion of win by difference in seeds")
plt.show()

# There isn’t a huge difference, but the slope between scorediff and seeddiff is less steep for the tournament games.
# This means that the games tend to be closer in the tournament than regular season, controlling for the difference in
# seeds. The difference in slopes might be used to quantify the increase in competitiveness in the tournament.
sns.lmplot(x='seeddiff', y='scorediff', hue='tourney', data=data, aspect=2)
plt.suptitle("Difference in scores by difference in seeds")
plt.show()

newData = data.loc[(data['tourney'] == 0)]
print(newData[['seednum1', 'seednum2']].loc[newData['seednum1'].notna() & newData['seednum2'].notna()])
print(data.loc[(data['tourney'] != 0)].shape)
print(data.loc[data['seeddiff'].notna()].shape)

# Similar result here as above, but for the logistic regression curve. The difference in seeds has less impact on the
# winning probabilities in the tournament than during regular season.
sns.lmplot(x='seeddiff', y='team1win', hue='tourney', data=data, scatter_kws={"s": 5}, y_jitter=0.03, logistic=True, aspect=1.5)
plt.suptitle("Win vs. Difference in seeds")
plt.show()

# When the losing team scores high, the games are more competitive in a sense that there’s less score difference.
# This is intuitive because there’s a soft threshold for the total points scored in a game due to the play-clock.
fig, axes = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10, 6))
axes[0].scatter(data['score_l'], data['score_w'], s=1)
axes[1].hexbin(data['score_l'], data['score_w'], bins='log', gridsize=50)
plt.subplots_adjust(left=0.1, bottom=0.2, right=None, top=None, wspace=0.05, hspace=None)
fig.text(0.5, 0.04, 'Losing Score', ha='center')
fig.text(0.04, 0.5, 'Winning Score', va='center', rotation='vertical')
plt.suptitle('Winning vs. Losing Scores')
plt.show()

# This plot shows the same information as the one above.
fig, axes = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10, 6))
axes[0].scatter(data['score_l'], data['scorediff'].abs(), s=1)
axes[1].hexbin(data['score_l'], data['scorediff'].abs(), bins='log', gridsize=50)
plt.subplots_adjust(left=0.1, bottom=0.2, right=None, top=None, wspace=0.05, hspace=None)
fig.text(0.5, 0.04, 'Losing Team Points', ha='center')
fig.text(0.04, 0.5, 'Score Difference', va='center', rotation='vertical')
plt.suptitle('Score Difference vs. Losing Score')
plt.show()

# How many times does a pair of teams play each other in a season?
# Only about 30% of all pairs play twice in a season. About 5.7% of all pairs play three times.
num_encounters = data.groupby(['team1', 'team2']).size().value_counts()
print(tabulate(pd.DataFrame({'num_encounters':num_encounters.index, 'count': num_encounters,
                    'prop': num_encounters / num_encounters.sum()}).set_index('num_encounters'), headers="keys"))

# Does the outcome of a regular season game between team1 and team2 predict the outcome in the tournament?
# In 2015, there’s only five regular season games between two teams that played in a tournament game.
# In four out of five cases, the outcome from the tournament agreed with the outcome from the regular season.
tourney_matchups = data.loc[data.tourney == 1]
regular_matchups = data.loc[data.tourney == 0]
joined_matchups = pd.merge(regular_matchups, tourney_matchups, on=['team1', 'team2'], suffixes=('_regular', '_tourney'))
print(tabulate(joined_matchups[['team1', 'team2', 'seednum1_tourney', 'seednum2_tourney', 'team1win_tourney',
                                'team1win_regular']], headers="keys"))