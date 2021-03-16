import pandas as pd
import os

def getTrainData():
    print("Preparing training data...")
    if os.path.exists("GameData_Complete.csv"):
        return pd.read_csv("GameData_Complete.csv")

    TourneyGames = pd.read_csv('Data\MNCAATourneyDetailedResults.csv')
    RegGames = pd.read_csv('Data\MRegularSeasonDetailedResults.csv')
    KenPom = pd.read_csv('KenPom.csv')

    TourneyGames['TourneyGame'] = 1
    RegGames['TourneyGame'] = 0

    AllGames = RegGames.append(TourneyGames).reset_index(drop=True)
    AllGames['TourneyGame'] = AllGames.pop('TourneyGame')
    AllGames['WFG'] = AllGames['WFGM'] / AllGames['WFGA']
    AllGames['WFG3'] = AllGames['WFGM3'] / AllGames['WFGA3']
    AllGames['WFT'] = AllGames['WFTM'] / AllGames['WFTA']
    AllGames['LFG'] = AllGames['LFGM'] / AllGames['LFGA']
    AllGames['LFG3'] = AllGames['LFGM3'] / AllGames['LFGA3']
    AllGames['LFT'] = AllGames['LFTM'] / AllGames['LFTA']

    toDrop = ['WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA']
    Team1_newFields = ['TeamID_1', 'Score_1', 'FG_1', 'FG3_1', 'FT_1', 'OR_1', 'DR_1', 'Ast_1', 'TO_1', 'Stl_1', 'Blk_1', 'PF_1']
    Team2_newFields = ['TeamID_2', 'Score_2', 'FG_2', 'FG3_2', 'FT_2', 'OR_2', 'DR_2', 'Ast_2', 'TO_2', 'Stl_2', 'Blk_2', 'PF_2']
    WTeam_oldFields = ['WTeamID', 'WScore', 'WFG', 'WFG3', 'WFT', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']
    LTeam_oldFields = ['LTeamID', 'LScore', 'LFG', 'LFG3', 'LFT', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']

    for new1, new2, oldW, oldL in zip(Team1_newFields, Team2_newFields, WTeam_oldFields, LTeam_oldFields):
        AllGames.loc[AllGames['WLoc'] == 'H', new1] = AllGames[oldW]
        AllGames.loc[AllGames['WLoc'] == 'A', new1] = AllGames[oldL]
        AllGames.loc[AllGames['WLoc'] == 'N', new1] = AllGames[oldW]
        AllGames.loc[AllGames['WLoc'] == 'H', new2] = AllGames[oldL]
        AllGames.loc[AllGames['WLoc'] == 'A', new2] = AllGames[oldW]
        AllGames.loc[AllGames['WLoc'] == 'N', new2] = AllGames[oldL]

    AllGames.drop(WTeam_oldFields + LTeam_oldFields + toDrop, axis=1, inplace=True)
    PomMetrics = ['conference', 'adjem', 'adjo', 'adjd', 'adjt', 'luck', 'oppos', 'oppds', 'adjemn', 'wpct', 'rank',
                  'seed', 'school', 'wins', 'losses', 'adjems']
    for team in ['_1', '_2']:
        AllGames = AllGames.merge(KenPom, left_on=['TeamID' + team, 'Season'], right_on=['TeamID', 'Season'], how='inner')
        for metric in PomMetrics:
            AllGames.rename(columns={metric: metric + team}, inplace=True)
        AllGames.drop(['TeamID', 'adjemnR', 'adjoR', 'adjdR', 'adjtR', 'luckR', 'adjemsR', 'opposR', 'oppdsR'], axis=1, inplace=True)

    AllGames = AllGames[['Season', 'DayNum', 'TourneyGame', 'school_1', 'TeamID_1', 'Score_1', 'school_2', 'TeamID_2',
                         'Score_2', 'rank_1', 'seed_1', 'conference_1', 'wins_1', 'losses_1', 'rank_2', 'seed_2',
                         'conference_2', 'wins_2', 'losses_2', 'WLoc', 'NumOT', 'FG_1', 'FG3_1', 'FT_1', 'OR_1', 'DR_1',
                         'Ast_1', 'TO_1', 'Stl_1', 'Blk_1', 'PF_1', 'FG_2', 'FG3_2', 'FT_2', 'OR_2', 'DR_2', 'Ast_2',
                         'TO_2', 'Stl_2', 'Blk_2', 'PF_2', 'wpct_1', 'adjem_1', 'adjo_1', 'adjd_1', 'adjt_1', 'luck_1',
                         'adjems_1', 'oppos_1', 'oppds_1', 'wpct_2', 'adjemn_1', 'adjem_2', 'adjo_2', 'adjd_2', 'adjt_2',
                         'luck_2', 'adjems_2', 'oppos_2', 'oppds_2', 'adjemn_2']]

    AllGames.round(3).to_csv("GameData_plus_KenPom.csv", index=False)
    ##################################################
    RegGames['WinsTop25'] = 0
    RegGames['WinsTop5'] = 0
    RegGames['WFG'] = RegGames['WFGM'] / RegGames['WFGA']
    RegGames['WFG3'] = RegGames['WFGM3'] / RegGames['WFGA3']
    RegGames['WFT'] = RegGames['WFTM'] / RegGames['WFTA']
    RegGames['LFG'] = RegGames['LFGM'] / RegGames['LFGA']
    RegGames['LFG3'] = RegGames['LFGM3'] / RegGames['LFGA3']
    RegGames['LFT'] = RegGames['LFTM'] / RegGames['LFTA']
    metrics = ['Score','FG','FG3','FT','TO','rank','wins','losses']

    for Win_Loss in ['W', 'L']:
        RegGames = RegGames.merge(KenPom[['Season', 'TeamID', 'rank', 'wins']], left_on=[Win_Loss + 'TeamID', 'Season'], right_on=['TeamID', 'Season'], how='left')
        RegGames.drop(['TeamID'], axis=1, inplace=True)
        RegGames.rename(columns={'rank': Win_Loss + 'rank'}, inplace=True)
        RegGames.rename(columns={'wins': Win_Loss + 'wins'}, inplace=True)

    WinTeamData = RegGames.drop(['LTeamID','WAst','LAst','LStl','WStl','LBlk','WBlk','LPF','WPF','NumOT','DayNum'], axis=1)
    WinTeamData.rename(columns={'Wschool': 'School'}, inplace=True)
    WinTeamData.rename(columns={'WTeamID': 'TeamID'}, inplace=True)
    WinTeamData.rename(columns={'Wwins': 'wins'}, inplace=True)
    WinTeamData.rename(columns={'Wlosses': 'losses'}, inplace=True)
    WinTeamData.loc[WinTeamData['Lrank'] <= 25, 'WinsTop25'] = 1
    WinTeamData.loc[WinTeamData['Lrank'] <= 5, 'WinsTop5'] = 1
    for metric in metrics:
        WinTeamData.rename(columns={'W'+metric: metric}, inplace=True)
        WinTeamData.rename(columns={'L'+metric: 'Opp'+metric}, inplace=True)

    LosingTeamData = RegGames.drop(['WTeamID','WAst','LAst','LStl','WStl','LBlk','WBlk','LPF','WPF','NumOT','DayNum'], axis=1)
    LosingTeamData.rename(columns={'Lschool': 'School'}, inplace=True)
    LosingTeamData.rename(columns={'LTeamID': 'TeamID'}, inplace=True)
    LosingTeamData.rename(columns={'Lwins': 'wins'}, inplace=True)
    LosingTeamData.rename(columns={'Llosses': 'losses'}, inplace=True)
    for metric in metrics:
        LosingTeamData.rename(columns={'L'+metric: metric}, inplace=True)
        LosingTeamData.rename(columns={'W'+metric: 'Opp'+metric}, inplace=True)

    TeamData = WinTeamData.append(LosingTeamData, ignore_index=True)
    TeamData['TOmargin'] = TeamData['TO'] - TeamData['OppTO']
    TeamData['PointMargin'] = TeamData['Score'] - TeamData['OppScore']
    TeamData = TeamData[['Season','TeamID','Score','wins','WinsTop25','WinsTop5','OppScore','FG','OppFG','FG3','OppFG3','FT','OppFT','TOmargin','PointMargin']]

    TeamData_means = TeamData.groupby(['TeamID','Season']).mean().reset_index()
    TeamData_means.drop(['WinsTop25','WinsTop5'], axis=1, inplace=True)
    TeamData_sums = TeamData.groupby(['TeamID','Season']).sum().reset_index()
    TeamData_sums.drop(['Score', 'OppScore', 'TOmargin', 'PointMargin', 'FG', 'OppFG', 'FG3', 'OppFG3', 'FT', 'OppFT','wins'], axis=1, inplace=True)

    SeasonMetrics = TeamData_means.merge(TeamData_sums, left_on=['TeamID','Season'], right_on = ['TeamID','Season'], how='outer').round(3)
    SeasonMetrics.insert(13, 'wins', SeasonMetrics.pop('wins'))
    SeasonMetrics.to_csv("SeasonMetrics.csv", index=False)

    KenPom_SeasonMetrics = KenPom.merge(SeasonMetrics.drop(['wins'], axis=1), left_on=['TeamID', 'Season'], right_on=['TeamID', 'Season'], how='outer')
    KenPom_SeasonMetrics.insert(10, 'WinsTop25', KenPom_SeasonMetrics.pop('WinsTop25'))
    KenPom_SeasonMetrics.insert(11, 'WinsTop5', KenPom_SeasonMetrics.pop('WinsTop5'))
    KenPom_SeasonMetrics.to_csv("KenPom_SeasonMetrics.csv", index=False)

    KenPom_gameData = AllGames
    for team in ['_1', '_2']:
        KenPom_gameData = KenPom_gameData.merge(SeasonMetrics, left_on=['TeamID' + team, 'Season'], right_on=['TeamID', 'Season'], how='inner')
        for field in SeasonMetrics.drop(['TeamID', 'Season', 'wins', 'TOmargin', 'PointMargin', 'WinsTop25', 'WinsTop5'], axis=1).columns:
            KenPom_gameData.rename(columns={field: 'Avg' + field + team}, inplace=True)
        KenPom_gameData.rename(columns={'TOmargin': 'TOmargin' + team}, inplace=True)
        KenPom_gameData.rename(columns={'PointMargin': 'PointMargin' + team}, inplace=True)
        KenPom_gameData.rename(columns={'WinsTop25': 'WinsTop25' + team}, inplace=True)
        KenPom_gameData.rename(columns={'WinsTop5': 'WinsTop5' + team}, inplace=True)
        KenPom_gameData.drop(['TeamID', 'wins'], axis=1, inplace=True)

    KenPom_gameData['HomeTeamWon'] = 0
    KenPom_gameData.loc[KenPom_gameData['Score_1'] > KenPom_gameData['Score_2'], 'HomeTeamWon'] = 1
    KenPom_gameData.drop(['WLoc'], axis=1, inplace=True)

    KenPom_gameData.round(3).to_csv("GameData_Complete.csv", index=False)

    return KenPom_gameData


if __name__ == '__main__':
    KenPom_gameData = getTrainData()

