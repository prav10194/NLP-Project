import nltk
from nltk import FreqDist
from nltk import word_tokenize
import os
from collections import defaultdict
import time
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse import stanford
from nltk.internals import find_jars_within_path
from pycorenlp import StanfordCoreNLP
import logging
import json
from nltk.stem.wordnet import WordNetLemmatizer
from tqdm import tqdm
from nltk.corpus import wordnet
import re

def get_documents():

    return os.listdir(os.getcwd()+"/corpus/")

def get_features(query):

    file_features = open("/CorpusFilesWithFeatures"+query.split('.')[0]+"_outputTask3.txt").read()
    file_features = file_features.replace("\n","<br>")
    print("FILE CONTENT: ")
    print(file_features)
    return file_features
