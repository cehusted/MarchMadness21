import matplotlib.pyplot as plt
import numpy as np


def plotPredHist(p, index):
    plt.figure(index)
    my_csv = np.genfromtxt(p, delimiter=',')
    bins_array = np.arange(0.0, 1.01, 0.05)
    id, pred = my_csv.transpose()

    plt.hist(pred, bins=bins_array, edgecolor='black')
    plt.xlim([0.0, 1.0])
    plt.xticks(np.arange(0.0, 1.1, 0.1))
    plt.title('Submission results distribution')
    plt.ylabel('Number of matches (Total = 2278)')
    plt.xlabel('Probability')
    plt.savefig("Predictions_histogram{}.png".format(index))

if __name__ == "__main__":
    file_path = 'Stage2_Submission_FT.csv'
    plotPredHist(file_path, 2)
