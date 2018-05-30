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
import json
import shutil

nlp = StanfordCoreNLP('http://localhost:9000')

input_query = "When will my OPT start processing?"
input_tokens = nltk.tokenize.word_tokenize(input_query)

tags_mapping = defaultdict(lambda: '')

tags_mapping['V'] = 'v'
tags_mapping['J'] = 'a'
tags_mapping['N'] = 'n'

##tags_mapping = {'V':'v','J':'a','N':'n','P':'n','M':'v','W':'v','D':'',':':'','I':'','C':''}

def return_sent_tokenize(text):
    return nltk.sent_tokenize(text)

def return_word_tokenize(text):
    return nltk.word_tokenize(text)

def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in words if not w in stop_words]
    return filtered_sentence

def lemmatization(words):
    lmtzr = WordNetLemmatizer()
    lemmatized_words = [lmtzr.lemmatize(i,j[0].lower()) if j[0].lower() in ['a','n','v'] else lmtzr.lemmatize(i) for i,j in nltk.tag.pos_tag(words)]
    return lemmatized_words


def stemming(words):
    sno = nltk.stem.SnowballStemmer('english')
    stem_list = []

    for word in words:
        stem_list.append(sno.stem(word))

    return stem_list


def pos_tags(words):
    return nltk.tag.pos_tag(words)

def parse_tree(sentences):

    parse_tree_string = []

    for sent in sentences:
        output = nlp.annotate(sent, properties={
          'annotators': 'depparse',
          'outputFormat': 'json'
        })
        # print(output['sentences'][0]['basicDependencies'])

        for parse_dict in output['sentences'][0]['basicDependencies']:
            for key, value in parse_dict.items():
                if key == 'dep':
                    parse_tree_string.append((key, value))
                if key == 'dependentGloss':
                    parse_tree_string.append((key, value))



    # print("parse_tree_string: "+str(parse_tree_string))

    return parse_tree_string

def extract_hypernyms(words):

    hypernyms_list_of_all_words = []

    for word in words:
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
            hypernyms_collection = s.hypernyms()
            for h in hypernyms_collection:
                hypernyms_list_of_all_words.append(h.name().split(".")[0])

    hypernyms_list_of_all_words = set(hypernyms_list_of_all_words)

    hypernyms_list_of_all_words = list(hypernyms_list_of_all_words)

    return hypernyms_list_of_all_words


def extract_hyponyms(words):

    hyponyms_list_of_all_words = []


    for word in words:
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
            hyponyms_collection = s.hyponyms()
            for h in hyponyms_collection:
                hyponyms_list_of_all_words.append(h.name().split(".")[0])

    hyponyms_list_of_all_words = set(hyponyms_list_of_all_words)

    hyponyms_list_of_all_words = list(hyponyms_list_of_all_words)

    return hyponyms_list_of_all_words


def extract_meronyms(words):

    meronyms_list_of_all_words = []

    for word in words:
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
            meronyms_collection = s.part_meronyms()
            meronyms_collection += s.substance_meronyms()
            meronyms_collection += s.member_meronyms()

            for h in meronyms_collection:
                meronyms_list_of_all_words.append(h.name().split(".")[0])
    meronyms_list_of_all_words = set(meronyms_list_of_all_words)

    meronyms_list_of_all_words = list(meronyms_list_of_all_words)

    return meronyms_list_of_all_words

def extract_holonyms(words):

    holonyms_list_of_all_words = []

    for word in words:
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
            holonyms_collection = s.part_holonyms()
            holonyms_collection += s.substance_holonyms()
            holonyms_collection += s.member_holonyms()

            for h in holonyms_collection:
                holonyms_list_of_all_words.append(h.name().split(".")[0])

    holonyms_list_of_all_words = set(holonyms_list_of_all_words)

    holonyms_list_of_all_words = list(holonyms_list_of_all_words)

    return holonyms_list_of_all_words


def extract_synonyms(words):

    synonyms_list_of_all_words = []

    for word in words:
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
            synonyms_list_of_all_words += s.lemma_names()

    synonyms_list_of_all_words = set(synonyms_list_of_all_words)

    synonyms_list_of_all_words = list(synonyms_list_of_all_words)

    return synonyms_list_of_all_words




# print("os.getcwd() "+str(os.getcwd()))

os.chdir(os.getcwd()+"/corpus/")

for filename in tqdm(os.listdir(os.getcwd())):
        if '.txt' in filename:
                content = open(filename, encoding='utf-8').read()

                old_content = content

                sentences = return_sent_tokenize(content)

                words = return_word_tokenize(content)

                words_without_stop_words = remove_stop_words(words)

                words_with_stemming = stemming(words_without_stop_words)

                words_with_lemmatization = lemmatization(words_without_stop_words)

                words_with_pos_tags = pos_tags(words_without_stop_words)


                parse_tree_string = parse_tree(sentences)

                hypernyms_list = extract_hypernyms(words_without_stop_words)

                hyponyms_list = extract_hyponyms(words_without_stop_words)

                meronyms_list = extract_meronyms(words_without_stop_words)

                holonyms_list = extract_holonyms(words_without_stop_words)

                synonyms_list = extract_synonyms(words_without_stop_words)

                file_write = open('../CorpusFilesWithFeatures/'+filename.split('.')[0] + "_outputTask3JSON.json",'w')

                # print('Filename: '+str(filename))

                features_dictionary = defaultdict()

                features_dictionary['question'] = re.findall(r'.*\?', old_content)[0]

                features_dictionary['answer'] = old_content.replace(re.findall(r'.*\?', old_content)[0],"")

                features_dictionary['sentence_tokenizer'] = sentences

                features_dictionary['words_tokenizer'] = words

                features_dictionary['words_without_stop_words'] = words_without_stop_words

                features_dictionary['words_with_stemming'] = words_with_stemming

                features_dictionary['words_with_lemmatization'] = words_with_lemmatization

                features_dictionary['words_with_pos_tags'] = words_with_pos_tags

                features_dictionary['parse_tree_string'] = parse_tree_string

                features_dictionary['hypernyms_list'] = hypernyms_list

                features_dictionary['hyponyms_list'] = hyponyms_list

                features_dictionary['meronyms_list'] = meronyms_list

                features_dictionary['holonyms_list'] = holonyms_list

                features_dictionary['synonyms_list'] = synonyms_list

                file_write.write(json.dumps(features_dictionary))

                file_write.close()

                file_write = open('../CorpusFilesWithFeatures/'+filename.split('.')[0] + "_outputTask3.txt",'w')
                file_write.write("Corpus Question: "+re.findall(r'.*\?', old_content)[0])
                file_write.write("\n\nCorpus Answer: "+(old_content.replace(re.findall(r'.*\?', old_content)[0],"")).encode('ascii', 'ignore').decode('ascii'))
                file_write.write("\n\nSentence Tokenizer: "+ str(sentences))
                file_write.write("\n\nWords Tokenizer: "+ str(words))
                file_write.write("\n\nwords_without_stop_words: "+ str(words_without_stop_words))
                file_write.write("\n\nwords_with_stemming: "+ str(words_with_stemming))
                file_write.write("\n\nwords_with_lemmatization: "+ str(words_with_lemmatization))
                file_write.write("\n\nwords_with_pos_tags: "+ str(words_with_pos_tags))
                file_write.write("\n\nparse_tree_string: "+ str(parse_tree_string))
                file_write.write("\n\nhypernyms_list: "+ str(hypernyms_list))
                file_write.write("\n\nhyponyms_list: "+ str(hyponyms_list))
                file_write.write("\n\nmeronyms_list: "+ str(meronyms_list))
                file_write.write("\n\nholonyms_list: "+ str(holonyms_list))
                file_write.write("\n\nsynonyms_list: "+ str(synonyms_list))
                file_write.close()

shutil.copytree("../CorpusFilesWithFeatures/", "../static/CorpusFilesWithFeatures")
