# Code to split the gospels in their traditions.
# Ycreak 2020-06-23
# import Packages
from nltk.tokenize import word_tokenize
import os

import pickle

from optparse import OptionParser
import sys
import json
# import pdb
from pudb import set_trace
import pandas as pd

from cltk.tag.pos import POSTag



from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from cltk.stop.greek.stops import STOPS_LIST

# import Classes
from Class_traditions import Traditions

# Command line parser base on the Classification of text documents using sparse 
# features program by Peter Prettenhofer, Olivier Grisel, Mathieu Blondel and Lars Buitinck
# License: BSD 3 clause
op = OptionParser()
op.add_option("--lemmatize",
              action="store_true", dest="lemmatize",
              help="Creates a lemmatized version of the entries.")
op.add_option("--traditions",
              action="store_true", dest="createTraditions",
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

# Find entries in given path.
path = "./TXT/Source/"

entries = []
for file in os.listdir(path):
    if file.endswith(".json"):
        entries.append(file)

def deleteTraditions():
  path = "./TXT/Output/"
  entries = []
  for file in os.listdir(path):
    if file.endswith(".txt"):
        entries.append(file)

  for file in entries:
    file = path + file
    os.remove(file)

def main():
  t = Traditions()

  # Fills the lists with separate books
  t.retrieveTraditions()
  # exit(0)
  # For every gospel, process its text.
  
  if opts.createTraditions:

    deleteTraditions() # Delete the files that where already there. Append problem.
    for entry in entries:
      file = path + entry

      author = t.retrieveName(file)

      if "luke" in file:
        t.processText(file, author)
        # lemmatizeText(file,author)
      elif "mark" in file:
        t.processText(file, author)
      elif "matthew" in file:
        t.processText(file, author)
      elif "john" in file:
        t.processText(file, author)        

  if opts.lemmatize:
    # Find entries in given path.
    t.createLemmatizedVersions()

main()
