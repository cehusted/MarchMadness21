import pandas as pd

TourneyGames = pd.read_csv('Data\MNCAATourneyDetailedResults.csv')
RegGames = pd.read_csv('Data\MRegularSeasonDetailedResults.csv')
KenPom = pd.read_csv('KenPom.csv')

TourneyGames['tourney_game'] = 1.0
RegGames['tourney_game'] = 0.0

AllGames = RegGames.append(TourneyGames)
AllGames.insert(8, 'WFGpct', AllGames['WFGM'] / AllGames['WFGA'])
AllGames.insert(9, 'WFG3pct', AllGames['WFGM3'] / AllGames['WFGA3'])
AllGames.insert(10, 'WFTpct', AllGames['WFTM'] / AllGames['WFTA'])
AllGames.insert(24, 'LFGpct', AllGames['LFGM'] / AllGames['LFGA'])
AllGames.insert(25, 'LFG3pct', AllGames['LFGM3'] / AllGames['LFGA3'])
AllGames.insert(26, 'LFTpct', AllGames['LFTM'] / AllGames['LFTA'])
AllGames[['WFGpct', 'WFG3pct', 'WFTpct', 'LFGpct', 'LFG3pct', 'LFTpct']] = AllGames[['WFGpct', 'WFG3pct', 'WFTpct', 'LFGpct', 'LFG3pct', 'LFTpct']].round(3)
AllGames.drop(['WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA'], axis=1, inplace=True)

#print("AllGames columns:", AllGames.columns)
#print("KenPom columns:", KenPom.columns)
print("Number of games available from each season:\n", AllGames['Season'].value_counts())

efficiency_list = ['conference', 'adjem', 'adjo', 'adjd', 'adjt', 'luck', 'oppos', 'oppds', 'adjemn', 'wpct', 'rank',
                   'seed', 'school', 'wins', 'losses', 'adjems']
for hr in ['W', 'L']:
    AllGames = AllGames.merge(KenPom, left_on=[hr+'TeamID', 'Season'], right_on=['TeamID', 'Season'], how='inner')
    for metric in efficiency_list:
        AllGames.rename(columns={metric: hr+metric}, inplace=True)
        #print(AllGames.columns)
    AllGames.drop(['TeamID', 'adjemnR', 'adjoR', 'adjdR', 'adjtR', 'luckR', 'adjemsR', 'opposR', 'oppdsR'], axis=1, inplace=True)

AllGames.insert(2, 'Wschool', AllGames.pop('Wschool'))
AllGames.insert(5, 'Lschool', AllGames.pop('Lschool'))
AllGames.insert(8, 'Wrank', AllGames.pop('Wrank'))
AllGames.insert(9, 'Wseed', AllGames.pop('Wseed'))
AllGames.insert(10, 'Wconference', AllGames.pop('Wconference'))
AllGames.insert(11, 'Wwins', AllGames.pop('Wwins'))
AllGames.insert(12, 'Wlosses', AllGames.pop('Wlosses'))
AllGames.insert(13, 'Lrank', AllGames.pop('Lrank'))
AllGames.insert(14, 'Lseed', AllGames.pop('Lseed'))
AllGames.insert(15, 'Lconference', AllGames.pop('Lconference'))
AllGames.insert(16, 'Lwins', AllGames.pop('Lwins'))
AllGames.insert(17, 'Llosses', AllGames.pop('Llosses'))

AllGames.to_csv("KenPom+gameData.csv", index=False)
##################################################

AllGames['WinsTop25'] = 0
AllGames['WinsTop5'] = 0
metrics = ['Score','FGpct','FG3pct','FTpct','TO','rank','wins','losses']

WinTeamData = AllGames.drop(['Lschool', 'LTeamID','WAst','LAst','LStl','WStl','LBlk','WBlk','LPF','WPF','NumOT','DayNum'], axis=1)
WinTeamData.rename(columns={'Wschool': 'School'}, inplace=True)
WinTeamData.rename(columns={'WTeamID': 'TeamID'}, inplace=True)
WinTeamData.rename(columns={'Wwins': 'wins'}, inplace=True)
WinTeamData.rename(columns={'Wlosses': 'losses'}, inplace=True)
WinTeamData.loc[WinTeamData['Lrank'] <= 25, 'WinsTop25'] = 1
WinTeamData.loc[WinTeamData['Lrank'] <= 5, 'WinsTop5'] = 1
for metric in metrics:
    WinTeamData.rename(columns={'W'+metric: metric}, inplace=True)
    WinTeamData.rename(columns={'L'+metric: 'Opp'+metric}, inplace=True)

LosingTeamData = AllGames.drop(['Wschool', 'WTeamID','WAst','LAst','LStl','WStl','LBlk','WBlk','LPF','WPF','NumOT','DayNum'], axis=1)
LosingTeamData.rename(columns={'Lschool': 'School'}, inplace=True)
LosingTeamData.rename(columns={'LTeamID': 'TeamID'}, inplace=True)
LosingTeamData.rename(columns={'Lwins': 'wins'}, inplace=True)
LosingTeamData.rename(columns={'Llosses': 'losses'}, inplace=True)
for metric in metrics:
    LosingTeamData.rename(columns={'L'+metric: metric}, inplace=True)
    LosingTeamData.rename(columns={'W'+metric: 'Opp'+metric}, inplace=True)

AllGames = WinTeamData.append(LosingTeamData, ignore_index=True)
AllGames['TOmargin'] = AllGames['TO'] - AllGames['OppTO']
AllGames['PointMargin'] = AllGames['Score'] - AllGames['OppScore']
AllGames = AllGames[['Season','TeamID','Score','wins','WinsTop25','WinsTop5','OppScore','FGpct','OppFGpct','FG3pct','OppFG3pct','FTpct','OppFTpct','TOmargin','PointMargin']]

AllGames_means = AllGames.groupby(['TeamID','Season']).mean().reset_index()
AllGames_means.drop(['WinsTop25','WinsTop5'], axis=1, inplace=True)
AllGames_sums = AllGames.groupby(['TeamID','Season']).sum().reset_index()
AllGames_sums.drop(['Score', 'OppScore', 'TOmargin', 'PointMargin', 'FGpct', 'OppFGpct', 'FG3pct', 'OppFG3pct', 'FTpct', 'OppFTpct','wins'], axis=1, inplace=True)

Team_Yearlies = AllGames_means.merge(AllGames_sums, left_on=['TeamID','Season'], right_on = ['TeamID','Season'], how='outer').round(3)
Team_Yearlies.insert(12, 'wins', Team_Yearlies.pop('wins'))
Team_Yearlies.to_csv("Team_Yearly_Summaries.csv", index=False)

KenPom_Yearlies = KenPom.merge(Team_Yearlies.drop(['wins'], axis=1), left_on=['TeamID', 'Season'], right_on=['TeamID', 'Season'], how='outer')
KenPom_Yearlies.insert(9, 'WinsTop25', KenPom_Yearlies.pop('WinsTop25'))
KenPom_Yearlies.insert(10, 'WinsTop5', KenPom_Yearlies.pop('WinsTop5'))
KenPom_Yearlies.to_csv("KenPom+Yearlies.csv", index=False)