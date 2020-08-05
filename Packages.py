import json
from nltk.tokenize import word_tokenize
import os

from optparse import OptionParser
import sys

# import pdb
from pudb import set_trace
import pandas as pd

from cltk.tag.pos import POSTag

import Packages
from Class_traditions import Traditions

from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from cltk.stop.greek.stops import STOPS_LIST

from cltk.ir.query import search_corpus
# from cltk.ir.query import greek_word2vec_cltk
from cltk.corpus.utils.importer import CorpusImporter
# import pickle
from cltk.corpus.readers import get_corpus_reader

from cltk.corpus.greek.alphabet import UPPER_ROUGH_ACUTE
from greek_accentuation.characters import base

from greek_accentuation.characters import add_diacritic
from greek_accentuation.characters import length, strip_length
from greek_accentuation.syllabify import syllabify, display_word
from greek_accentuation.syllabify import is_diphthong
from greek_accentuation.syllabify import ultima, rime, onset_nucleus_coda
from greek_accentuation.syllabify import debreath, rebreath
from greek_accentuation.syllabify import syllable_length, syllable_accent
from greek_accentuation.syllabify import add_necessary_breathing
from greek_accentuation.accentuation import get_accent_type, display_accent_type
from greek_accentuation.accentuation import syllable_add_accent, make_paroxytone
from greek_accentuation.accentuation import possible_accentuations
from greek_accentuation.accentuation import recessive, on_penult

from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths


from cltk.corpus.greek.tlg.parse_tlg_indices import get_female_authors
from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithet_index
from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithets
from cltk.corpus.greek.tlg.parse_tlg_indices import select_authors_by_epithet
from cltk.corpus.greek.tlg.parse_tlg_indices import get_epithet_of_author
from cltk.corpus.greek.tlg.parse_tlg_indices import get_geo_index
from cltk.corpus.greek.tlg.parse_tlg_indices import get_geographies
from cltk.corpus.greek.tlg.parse_tlg_indices import select_authors_by_geo
from cltk.corpus.greek.tlg.parse_tlg_indices import get_geo_of_author
from cltk.corpus.greek.tlg.parse_tlg_indices import get_lists
from cltk.corpus.greek.tlg.parse_tlg_indices import get_id_author
from cltk.corpus.greek.tlg.parse_tlg_indices import select_id_by_name

from cltk.corpus.utils.formatter import assemble_tlg_works_filepaths

from cltk.stem.lemma import LemmaReplacer

from cltk.corpus.greek.tlgu import TLGU
from cltk.vector.word2vec import get_sims

from cltk.corpus.greek import tlg
from cltk.utils import philology
# tlg.compile()
import unicodedata
import matplotlib.pyplot as plt
 
# from tsne import tsne #Import the t-SNE algorithm

from sklearn.manifold import TSNE
from cltk.tokenize.greek.sentence import SentenceTokenizer

import re
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.stop.greek.stops import STOPS_LIST

from gensim import models
from gensim.models import Word2Vec, KeyedVectors
from cltk.vector.word2vec import get_sims

# import jieba 
from gensim import corpora

from gensim.models import Word2Vec
from joblib import Parallel, delayed
import multiprocessing

from cltk.corpus.utils.formatter import cltk_normalize

import nltk
from nltk import word_tokenize

# from MulticoreTSNE import MulticoreTSNE as TSNE
from sklearn.decomposition import PCA #Grab PCA functions

import resource

import numpy as np
from gensim import models


#for visualization
import math
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sPCA
from sklearn import manifold #MSD, t-SNE