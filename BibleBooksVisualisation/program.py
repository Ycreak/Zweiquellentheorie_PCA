import pandas as pd
import matplotlib.pyplot as plt

from optparse import OptionParser
import sys
import numpy as np

import pickle

from sklearn.decomposition import PCA

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

import nltk
from nltk.corpus import stopwords

# Local file with all the bible books in an array
import biblebooks

pd.set_option('display.max_rows', None)

# Command line parser base on the Classification of text documents using sparse
# features program by Peter Prettenhofer, Olivier Grisel, Mathieu Blondel and Lars Buitinck
# License: BSD 3 clause
op = OptionParser()
op.add_option("--redoVect",
              action="store_true", dest="redoVect",
              help="Creates new Vect data in pickle form.")
op.add_option("--plotBooks",
              action="store_true", dest="plotBooks",
              help="Create plot of Books.")
op.add_option("--plotChapters",
              action="store_true", dest="plotChapters",
              help="Create plot of chapters.")
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

# Dumps given data in the given filename for later use
def dumpPickle(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def runProgram(df, file):
    # Remove all stop words (very necessary!)
    for t in stopwords.words('english'):
        df.t = [s.replace(' ' + t + ' ', ' ') for s in df.t]

    # Group by book and create a new dataframe with book and text (and an index)
    df_perBook = df.groupby(['b'])['t'].apply('  '.join).reset_index()
    df_perChapter = df.groupby(['b','c'])['t'].apply('  '.join).reset_index()

    # Add a column for the Testament
    df_perBook['testament'] = 0
    df_perChapter['testament'] = 0

    # The first 39 books are the Old Testament, the following the New one
    firstMat = df_perBook.loc[df_perBook['b'] == 40, :].index[0]
    df_perBook.loc[firstMat:, 'testament'] = 1

    firstMat = df_perChapter.loc[df_perChapter['b'] == 40, :].index[0]
    df_perChapter.loc[firstMat:, 'testament'] = 1

    if opts.plotBooks:
        # Vecotrizer
        vec = TfidfVectorizer()
        vecRes = vec.fit_transform(df_perBook.t).toarray()

        # PCA creation
        dr = PCA(n_components=2)
        pcaDF = pd.DataFrame(dr.fit_transform(vecRes))

        # Some magic I do not understand
        testament = df_perBook.groupby(['b'])[['testament']].agg('mean')
        testament.index = range(0,66)
        bookNames = df_perBook.groupby(['b']).agg('sum').index

        # Initialize the plot
        fig = plt.figure()
        fig.set_size_inches(14, 8)

        pcaDF = pd.DataFrame(dr.fit_transform(vecRes))
        plt.scatter(pcaDF.loc[testament.testament == 0, 0], pcaDF.loc[testament.testament == 0, 1], label='Old')
        plt.scatter(pcaDF.loc[testament.testament == 1, 0], pcaDF.loc[testament.testament == 1, 1], label='New')

        # Annotate the datapoints with the name of the corresponding book
        for p in pcaDF.index:
            plt.annotate(biblebooks.books[p], (pcaDF.loc[p, 0], pcaDF.loc[p, 1]))

        # Some Plot options
        titlePlt = 'Books PCA'+file
        plt.title(titlePlt)
        plt.legend()
        plt.show()

    if opts.plotChapters:
        # Vecotrizer
        vec = TfidfVectorizer()
        vecRes = vec.fit_transform(df_perChapter.t).toarray()

        # PCA creation
        dr = PCA(n_components=2)
        pcaDF = pd.DataFrame(dr.fit_transform(vecRes))

        fig = plt.figure() #.subplots(nrows=2, ncols=1)
        fig.set_size_inches(14, 12)

        # Chapters
        plt.scatter(pcaDF.loc[df_perChapter.testament == 0, :].iloc[:, 0], pcaDF.loc[df_perChapter.testament == 0, :].iloc[:, 1], label='Old')
        plt.scatter(pcaDF.loc[df_perChapter.testament == 1, :].iloc[:, 0], pcaDF.loc[df_perChapter.testament == 1, :].iloc[:, 1], label='New')
        plt.legend()

        for p in pcaDF.index:
            book = df_perChapter.b[p] - 1
            chapter = df_perChapter.c[p]
            string = str(book+1) + biblebooks.books[book] + str(chapter)
            plt.annotate(string, (pcaDF.loc[p, 0], pcaDF.loc[p, 1]))

        plt.show()

        print('Execution finished')

# Read the CSV file

import glob
path = './CSV/*.csv'
files = glob.glob(path)

for file in files:
    print(file)
    df = pd.read_csv(file)
    runProgram(df, file)

