import nltk
from nltk import FreqDist
from nltk import word_tokenize
import os
from collections import defaultdict
import time

def get_text(filename):
    text = open("corpus/"+filename, encoding='utf-8').read()
    return text

def find_documents(query):


    input_query = query
    input_tokens = nltk.tokenize.word_tokenize(input_query)
    input_fdist=FreqDist(input_tokens)

    print(type(input_fdist))

    for filename in os.listdir(os.getcwd()+"/corpus/"):
            if '.txt' in filename:
                    # print(filename)
                    content = open("corpus/"+filename, encoding='utf-8').read()
                    tokens = nltk.tokenize.word_tokenize(content)
                    fdist=FreqDist(tokens)
                    bagOfWords = open("CorpusFilesWithoutFeatures/"+filename.split(".")[0]+"_bagOfWords.txt",'w')
                    for key, value in fdist.items():
                            key = key.encode('utf-8')
                            key = key.decode('utf-8')
    ##                        print(key)
                            bagOfWords.write(key+":"+str(value)+"\n")
                    bagOfWords.close()



    ##Reading the files and converting them into a dictionary

    filename_with_score = defaultdict()

    for filename in os.listdir(os.getcwd()+"/CorpusFilesWithoutFeatures/"):
            if '.txt' in filename:
                    text = open("CorpusFilesWithoutFeatures/"+filename).readlines()
                    dict_corpus = defaultdict()
                    for t in text:
                            dict_corpus[t.split(":")[0]] = t.split(":")[1]
                    matches = 0
                    total_count = 0
                    for key_i, value_i in input_fdist.items():
                        for key_j, value_j in dict_corpus.items():
                            if key_i == key_j:
                                matches += 1
                                total_count += int(value_j)
                                filename_with_score[filename] = [matches, total_count]

    ##                print count, count2

    ##for key, value in filename_with_score.items():
    ##        print(str(key)+"\t"+str(value))

    filename_with_score_sorted = sorted(filename_with_score, key=lambda k: (filename_with_score[k][0], filename_with_score[k][1]), reverse=True)

    filename_with_score_sorted = filename_with_score_sorted[0:10]

    # for value in filename_with_score_sorted:
    #         print(str(value))

    top_ten_documents = defaultdict()

    i = 1
    for value in filename_with_score_sorted:
            value = value.replace('_bagOfWords','')
            top_ten_documents[i] = value
            i = i+1

    return top_ten_documents




##def deleteFiles():
##        for filename in os.listdir(os.getcwd()):
##                if '_bagOfWords' in filename:
##                        os.remove(filename)
##
##for filename in os.listdir(os.getcwd()):
##        if '_bagOfWords' in filename:
##                deleteFiles()
