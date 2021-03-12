import pandas as pd

TourneyGames = pd.read_csv('Data\MNCAATourneyDetailedResults.csv')
RegGames = pd.read_csv('Data\MRegularSeasonDetailedResults.csv')
KenPom = pd.read_csv('KenPom.csv')

TourneyGames['tourney_game'] = 1.0


RegGames['tourney_game'] = 0.0



AllGames = RegGames.append(TourneyGames)
print(AllGames.head())

print(AllGames['Season'].value_counts())
print(AllGames['WLoc'])

efficiency_list = ['conference','adjem','adjo','adjd','adjt','luck','oppos','oppds','adjemn']
for hr in ['W', 'L']:
    AllGames = pd.merge(AllGames, KenPom, left_on=[hr+'TeamID','Season'], right_on=['TeamID','Season'], how='inner')
    for metric in efficiency_list:
        AllGames.rename(columns={metric: hr+metric}, inplace=True)
    #AllGames = AllGames.drop(['TeamID','school'], axis=1)

print(AllGames.head())
print(AllGames.columns)