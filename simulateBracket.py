import pandas as pd
import numpy as np

def simulate(p):
    season = 2021
    seeds = pd.read_csv(r"Data\MNCAATourneySeeds.csv")
    seeds = seeds[seeds['Season'] == season].drop(['Season'], axis=1)
    slots = pd.read_csv(r"Data\MNCAATourneySlots.csv")
    slots = slots[slots['Season'] == season].drop(['Season'], axis=1)
    teams = pd.read_csv(r"Data\MTeams.csv")[['TeamID', 'TeamName']]

    # Simulate play-in games
    for playIn in ['W11', 'W16', 'X11', 'X16']:
        team1 = str(seeds.loc[seeds['Seed'] == '{}a'.format(playIn), 'TeamID'].tolist()[0])
        team2 = str(seeds.loc[seeds['Seed'] == '{}b'.format(playIn), 'TeamID'].tolist()[0])
        if team1 > team2:
            tmp = team2
            team2 = team1
            team1 = tmp
        assert(team1 < team2)
        team1_Odds = p.loc[p['ID'] == str(2021) + '_' + team1 + '_' + team2, 'Pred'].tolist()[0]
        winner = team1 if np.random.rand() < team1_Odds else team2
        seeds = seeds.append({'Seed': '{}'.format(playIn), 'TeamID': winner}, ignore_index=True)

    seeds = seeds[seeds['Seed'].apply(len) == 3].reset_index(drop=True)

    # Simulate First Round up to Final 4
    rounds = {1: 'First Round', 2: 'Round of 32', 3: 'Sweet 16', 4: 'Elite 8'}
    gameWinners = seeds.set_index('Seed').to_dict()['TeamID']
    for round, roundName in rounds.items():
        print("\n################### {} Predictions ###################".format(roundName))
        for region in ['W', 'X', 'Y', 'Z']:
            for game in range(8 // (2 ** (round - 1))):
                slot = 'R' + str(round) + region + str(game + 1)
                team1 = str(gameWinners[slots.loc[slots['Slot'] == slot, 'StrongSeed'].values[0]])
                team2 = str(gameWinners[slots.loc[slots['Slot'] == slot, 'WeakSeed'].values[0]])
                if team1 > team2:
                    tmp = team2
                    team2 = team1
                    team1 = tmp
                assert(team1 < team2)

                team1_Odds = p.loc[p['ID'] == str(2021) + '_' + team1 + '_' + team2, 'Pred'].tolist()[0]
                winner = team1 if np.random.rand() < team1_Odds else team2

                team1Name = teams.loc[teams['TeamID'] == int(team1), 'TeamName'].values[0]
                team2Name = teams.loc[teams['TeamID'] == int(team2), 'TeamName'].values[0]
                winnerName = teams.loc[teams['TeamID'] == int(winner), 'TeamName'].values[0]
                print("{} ({}%) vs. {}..... {}".format(team1Name, np.round(100 * team1_Odds, 1), team2Name, winnerName.upper()))

                gameWinners[slot] = winner

    # Simulate Final 4
    print("\n################### Final Four Predictions ###################".format(roundName))
    for slotFF in ['R5WX', 'R5YZ']:
        team1 = str(gameWinners[slots.loc[slots['Slot'] == slotFF, 'StrongSeed'].values[0]])
        team2 = str(gameWinners[slots.loc[slots['Slot'] == slotFF, 'WeakSeed'].values[0]])
        if team1 > team2:
            tmp = team2
            team2 = team1
            team1 = tmp
        assert (team1 < team2)

        team1_Odds = p.loc[p['ID'] == str(2021) + '_' + team1 + '_' + team2, 'Pred'].tolist()[0]
        winner = team1 if np.random.rand() < team1_Odds else team2

        team1Name = teams.loc[teams['TeamID'] == int(team1), 'TeamName'].values[0]
        team2Name = teams.loc[teams['TeamID'] == int(team2), 'TeamName'].values[0]
        winnerName = teams.loc[teams['TeamID'] == int(winner), 'TeamName'].values[0]
        print("{} ({}%) vs. {}..... {}".format(team1Name, np.round(100 * team1_Odds, 1), team2Name, winnerName.upper()))

        gameWinners[slotFF] = winner

    # Simulate Championship Game
    print("\n################### Championship Predictions ###################".format(roundName))
    if gameWinners['R5WX'] < gameWinners['R5YZ']:
        team1 = gameWinners['R5WX']
        team2 = gameWinners['R5YZ']
    else:
        team1 = gameWinners['R5YZ']
        team2 = gameWinners['R5WX']

    team1_Odds = p.loc[p['ID'] == str(2021) + '_' + team1 + '_' + team2, 'Pred'].tolist()[0]
    winner = team1 if np.random.rand() < team1_Odds else team2

    team1Name = teams.loc[teams['TeamID'] == int(team1), 'TeamName'].values[0]
    team2Name = teams.loc[teams['TeamID'] == int(team2), 'TeamName'].values[0]
    winnerName = teams.loc[teams['TeamID'] == int(winner), 'TeamName'].values[0]
    print("{} ({}%) vs. {}..... {}".format(team1Name, np.round(100 * team1_Odds, 1), team2Name, winnerName.upper()))

    gameWinners['R6CH'] = winner
    return winnerName

if __name__ == "__main__":
    # Supply path to your own predictions file
    predictions = pd.read_csv(r"Stage2_Submission_decent2.csv")
    winner = simulate(predictions)
    print("\n --- {} is your predicted winner! ---".format(winner))