import pandas as pd
import matplotlib.pyplot as plt

from optparse import OptionParser
import sys
import numpy as np

import pickle

from sklearn.decomposition import PCA


# import sklearn
# from sklearn.feature_extraction.text import TfidfTransformer
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Command line parser base on the Classification of text documents using sparse
# features program by Peter Prettenhofer, Olivier Grisel, Mathieu Blondel and Lars Buitinck
# License: BSD 3 clause
op = OptionParser()
op.add_option("--redoVect",
              action="store_true", dest="redoVect",
              help="Creates new Vect data in pickle form.")
op.add_option("--printResults",
              action="store_true", dest="printResults",
              help="Does what it says on the tin.")
op.add_option("--POSTagger",
              action="store_true", dest="POSTagger",
              help="Reruns the POSTagger.")
op.add_option("--Progress",
              action="store_true", dest="Progress",
              help="Prints progress of the program.")

#########################
# Option Parser Content #
#########################
def is_interactive():
    return not hasattr(sys.modules['__main__'], '__file__')

# work-around for Jupyter notebook and IPython console
argv = [] if is_interactive() else sys.argv[1:]
(opts, args) = op.parse_args(argv)
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)

print(__doc__)
op.print_help()
print()

########
# CODE #
########
import csv

teller = 1
arrayB = []

# with open("t_asv.csv", "r") as f:
    # reader = csv.DictReader(f, delimiter=",")
    # for row in reader:
        # # teller = row['b']
        # if teller == row['b']:
            # # print(row['b'],row['t'])
           # print('hello: ', row['b'])

# with open('protagonist.csv', 'w', newline='') as file:
    # writer = csv.writer(file)
    # writer.writerows(row_list)

def dumpPickle(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

df = pd.read_csv('t_asv.csv')

print(df['t'])

# print(df)
# exit(0)


# print(df)
# exit(0)


df_perChapter = df.groupby(['b'])['t'].apply('  '.join).reset_index()
# print(df_perChapter)

df_perChapter['testament'] = 0
# print(df_perChapter)

firstMat = df_perChapter.loc[df_perChapter['b'] == 40, :].index[0]
df_perChapter.loc[firstMat:, 'testament'] = 1


# print(df.b)
# print(df_perChapter)
# exit(0)

if opts.redoVect:
    if opts.Progress:
        print("Redoing Vectorization")

    vec = TfidfVectorizer()
    vecRes = vec.fit_transform(df_perChapter.t).toarray()
    simRes = cosine_similarity(vecRes)

    # vecRes = "helo"
    # simRes = "helo1"

    dumpPickle('vecRes.pickle',vecRes)
    dumpPickle('simRes.pickle',simRes)
else:
    if opts.Progress:
        print("Loading Pickle Files")
    vesRes = pickle.load('vecRes.pickle')
    simRes = pickle.load('simRes.pickle')

if opts.Progress:
    print("Melting")
# chaptersSim = pd.melt(pd.DataFrame(simRes)).value.drop_duplicates()

# if opts.Progress:
    # print("Creating Plot")
# fig, ax = plt.subplots(nrows=1, ncols=2)

# chaptersSim.hist(ax=ax[0])
# ax[0].set_title('Books')

# plt.show()

dr = PCA(n_components=2)
pcaDF = pd.DataFrame(dr.fit_transform(vecRes))
# pcaDF_books = pd.DataFrame(dr.fit_transform(vecRes_books))

fig, ax = plt.subplots(nrows=2, ncols=1)
fig.set_size_inches(14, 12)

ax[0].scatter(pcaDF.loc[df_perChapter.testament == 0, :].iloc[:, 0], pcaDF.loc[df_perChapter.testament == 0, :].iloc[:, 1], label='Old')
ax[0].scatter(pcaDF.loc[df_perChapter.testament == 1, :].iloc[:, 0], pcaDF.loc[df_perChapter.testament == 1, :].iloc[:, 1], label='New')
ax[0].set_title('Books PCA')
ax[0].legend()

# Chapters
# ax[0].scatter(pcaDF, pcaDF)
# ax[0].scatter(pcaDF.iloc[:, 0], pcaDF.iloc[:, 1])
# ax[0].scatter(pcaDF.loc[df.testament == 1, :].iloc[:, 0], pcaDF.loc[df.testament == 1, :].iloc[:, 1], label='New')
# ax[0].set_title('Chapters PCA')
# ax[0].legend()

plt.show()

# for row in df:
    # print(df.b, df.t)

# print((df.t).toarray())

# with open("t_asv.csv") as f:
    # for line in f:
        # for item in line:
            # print(item) #print(line)


