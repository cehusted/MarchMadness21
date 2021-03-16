import pandas as pd

def getTestData():
    print("Preparing test data...")
    Seeds = pd.read_csv('Data\MNCAATourneySeeds.csv')
    Seeds = Seeds[Seeds['Season']==2019]
    Seeds = Seeds.merge(Seeds, how='inner', on='Season', suffixes=('_x', '_y'))
    Seeds = Seeds[Seeds['TeamID_x'] < Seeds['TeamID_y']]

    Seeds['ID'] = Seeds['Season'].astype(str) + '_' + Seeds['TeamID_x'].astype(str) + '_' + Seeds['TeamID_y'].astype(str)
    Seeds['Seed_x'] = [int(x[1:3]) for x in Seeds['Seed_x']]
    Seeds['Seed_y'] = [int(x[1:3]) for x in Seeds['Seed_y']]

    Seeds.loc[Seeds['Seed_x'] <= Seeds['Seed_y'], 'TeamID_1'] = Seeds['TeamID_x']
    Seeds.loc[Seeds['Seed_x'] > Seeds['Seed_y'], 'TeamID_1'] = Seeds['TeamID_y']
    Seeds.loc[Seeds['Seed_x'] <= Seeds['Seed_y'], 'TeamID_2'] = Seeds['TeamID_y']
    Seeds.loc[Seeds['Seed_x'] > Seeds['Seed_y'], 'TeamID_2'] = Seeds['TeamID_x']

    Seeds.loc[Seeds['Seed_x'] <= Seeds['Seed_y'], 'Seed_1'] = Seeds['Seed_x']
    Seeds.loc[Seeds['Seed_x'] > Seeds['Seed_y'], 'Seed_1'] = Seeds['Seed_y']
    Seeds.loc[Seeds['Seed_x'] <= Seeds['Seed_y'], 'Seed_2'] = Seeds['Seed_y']
    Seeds.loc[Seeds['Seed_x'] > Seeds['Seed_y'], 'Seed_2'] = Seeds['Seed_x']
    Seeds['TourneyGame'] = 1

    TourneyData = Seeds.drop(['TeamID_x','TeamID_y','Seed_x','Seed_y'], axis=1)
    TourneyData[['TeamID_1', 'TeamID_2', 'Seed_1', 'Seed_2']] = TourneyData[['TeamID_1', 'TeamID_2', 'Seed_1', 'Seed_2']].astype('int')

    KenPom = pd.read_csv('KenPom.csv')
    SeasonMetrics = pd.read_csv("SeasonMetrics.csv")
    for team in ['_1', '_2']:
        TourneyData = TourneyData.merge(SeasonMetrics.drop(['wins'], axis=1), left_on=['Season', 'TeamID' + team], right_on=['Season', 'TeamID'], how='left', suffixes=('_1', '_2'))
        for field in SeasonMetrics.drop(['TeamID', 'Season', 'wins', 'TOmargin', 'PointMargin', 'WinsTop25', 'WinsTop5'], axis=1).columns:
            TourneyData.rename(columns={field: 'Avg' + field + team}, inplace=True)
        TourneyData.drop(['TeamID'], axis=1, inplace=True)
        TourneyData = TourneyData.merge(KenPom, left_on=['TeamID' + team, 'Season'], right_on=['TeamID', 'Season'], how='left', suffixes=('_1', '_2'))
        TourneyData.drop(['TeamID', 'adjemnR', 'adjoR', 'adjdR', 'adjtR', 'luckR', 'adjemsR', 'opposR', 'oppdsR'], axis=1, inplace=True)

    TourneyData.to_csv("TourneyData.csv", index=False)

    return TourneyData

if __name__ == '__main__':
    TourneyData = getTestData()
    print(TourneyData)
    print(TourneyData.columns)



