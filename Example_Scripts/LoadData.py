from tabulate import tabulate
import pandas as pd

RegularSeasonCompactResults = pd.read_csv('../Data/MRegularSeasonCompactResults.csv')         # (161552, 8)
print(tabulate(RegularSeasonCompactResults.head(), headers="keys"))

NCAATourneyCompactResults = pd.read_csv('../Data/MNCAATourneyCompactResults.csv')             # (2251, 8)
print(tabulate(NCAATourneyCompactResults.head(), headers="keys"))

NCAATourneySeeds = pd.read_csv('../Data/MNCAATourneySeeds.csv')                               # (2286, 3)
print(tabulate(NCAATourneyCompactResults.head(), headers="keys"))

Seasons = pd.read_csv('../Data/MSeasons.csv')                                                 # (36, 6)
print(tabulate(Seasons.head(), headers="keys"))

Teams = pd.read_csv('../Data/MTeams.csv')                                                     # (367, 4)
print(tabulate(Teams.head(), headers="keys"))

SampleSubmissionStage1 = pd.read_csv('../Data/MSampleSubmissionStage1_2020.csv')
print(tabulate(SampleSubmissionStage1.head(), headers="keys"), SampleSubmissionStage1.shape)

RegularSeasonDetailedResults = pd.read_csv('../Data/MRegularSeasonDetailedResults.csv')       # (87504, 34)
print(tabulate(RegularSeasonDetailedResults.head(), headers="keys"))

NCAATourneyDetailedResults = pd.read_csv('../Data/MNCAATourneyDetailedResults.csv')           # (1115, 34)
print(tabulate(NCAATourneyDetailedResults.head(), headers="keys"))

Cities = pd.read_csv('../Data/Cities.csv')                                                    # (435, 3)
print(tabulate(Cities.head(), headers="keys"))

GameCities = pd.read_csv('../Data/MGameCities.csv')                                           # (54838, 6)
print(tabulate(GameCities.head(), headers="keys"))

MasseyOrdinals = pd.read_csv('../Data/MMasseyOrdinals.csv')                                   # (3820919, 5)
print(tabulate(MasseyOrdinals.head(), headers="keys"))

Events_2015 = pd.read_csv('../Data/Events_2015.csv')
print(tabulate(Events_2015.head(), headers="keys"), Events_2015.shape)

Players_2015 = pd.read_csv('../Data/Players_2015.csv')
print(tabulate(Players_2015.head(), headers="keys"), Players_2015.shape)

ConferenceTourneyGames = pd.read_csv('../Data/MConferenceTourneyGames.csv')                   # (5149, 5)
print(tabulate(ConferenceTourneyGames.head(), headers="keys"))

TeamCoaches = pd.read_csv('../Data/MTeamCoaches.csv')                                         # (11348, 5)
print(tabulate(TeamCoaches.head(), headers="keys"))

Conferences = pd.read_csv('../Data/Conferences.csv')                                          # (51, 2)
print(tabulate(Conferences.head(), headers="keys"))

TeamConferences = pd.read_csv('../Data/MTeamConferences.csv')                                 # (11594, 3)
print(tabulate(TeamConferences.head(), headers="keys"))

SecondaryTourneyTeams = pd.read_csv('../Data/MSecondaryTourneyTeams.csv')                     # (1642, 3)
print(tabulate(SecondaryTourneyTeams.head(), headers="keys"))

SecondaryTourneyCompactResults = pd.read_csv('../Data/MSecondaryTourneyCompactResults.csv')   # (1624, 9)
print(tabulate(SecondaryTourneyCompactResults.head(), headers="keys"))

NCAATourneySlots = pd.read_csv('../Data/MNCAATourneySlots.csv')                               # (2251, 4)
print(tabulate(NCAATourneySlots.head(), headers="keys"))

NCAATourneySeedRoundSlots = pd.read_csv('../Data/MNCAATourneySeedRoundSlots.csv')             # (720, 5)
print(tabulate(NCAATourneySeedRoundSlots.head(), headers="keys"))
