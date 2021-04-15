# MarchMadness21
Developing a neural network predictor for 2021's March Madness Tournament

In order to run, the following is needed:
* "Data" folder
* main.py
* getKenPom.py
* prepare_data.py
* test_data.py
* Histogram_results.py
* simulateBracket.py

## Instructions
Run "main.py". This will gather data from KenPom, preprocess all of the data, organize training/testing data, train a NN model, produce submission files, and simulate the tournament based on the predictions. Several intermediate files will be created & saved along the way.
<br />Below are short descriptions of each of the scripts.

### main.py
The master script. Gathers/prepares all data, runs the training, creates submissions files. First submission file is raw values, second submission file takes every prediction within [0.4, 0.6] and pushes them toward the extremes.
<br />Files created:
* Stage2_Submission.csv
* Stage2_Submission_post.csv (a post-processed version of the first file)
### getKenPom.py
If no local "KenPom.csv", scrapes the KenPom website for 2002-2021 data and preprocesses it before saving it in project directory.
<br />Files created:
* KenPom.csv
### prepare_data.py
Takes KenPom.csv, Tourney Detailed Results, and Season Detailed Results and combines them together. More preprocessing, and several new metrics calculated here.
<br />Files created:
* GameData_plus_KenPom.csv (Detailed game data merged with KenPom metrics)
* SeasonMetrics.csv (Season-long/Season-average stats calculated out for every team)
* KenPom_SeasonMetrics.csv (Season stats merged with KenPom metrics)
* GameData_Complete (Training data in it's final format)
### test_data.py
Prepares test data for each possible matchup
<br />Files created:
* TourneyData.csv
### Histogram_Results.py
Receives a submission file as input, and saves to disk a histogram of all the predicted values. Gives a sense of how extreme the model is predicting overall.
<br />Files created:
* Predictions_histogram1.png
* Predictions_histogram2.png
### simulateBracket.py
Recieves a submission file as input, and simulates the entire tournament based on the probabilities. Displays probabilities and winners at each stage.
<br />Files created:
* None

# Submisisons 
Our first submission ("Stage2_Submission1.csv") was one that appeared to be well-balanced in terms of histogram probabilites. The following metrics were used in training (both for the "home" and "away" teams, so effectively twice the length of this list):
* Average Points Scored
* Average FG%
* Average Opposing FG%
* Average 3-PT%
* Average Turnover Margin
* Average Points Margin
* Wins
* Losses
* Adjusted Offensive Effiency (KenPom)
* Adjusted Defensive Efficiency (KenPom)
* Luck (KenPom)
* Adjusted opposing offensive strength (KenPom)
* Adjusted opposing defensive strength (KenPom)
* Rank in AP Poll
* Number of Top-25 wins
* Winning Percentage

Our second submission ("Stage2_Submission_FT.csv") was what we call a meme submission. It used the following features
* Free-Throw%
* Opposing Free-Throw%
* Adjusted Effeciency Margin (KenPom)

Both submissions had post-processing applied, meaning that every prediction within [0.4, 0.6] was pushed them toward the extremes by a 0.1 offset.

# Results
Submission 1 finished with a score of 0.66091<br />
Submission 2 finished with a score of 0.68700<br />
This was good for 504/707. Not exactly a position to be proud of, but still beat the baseline. We'll be back at it next year!

## Things to improve upon
* More tools to gauge feature importance
* More Visualization tools
* Further experimentation with NN architecture
