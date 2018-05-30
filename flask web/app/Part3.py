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
import time

nlp = StanfordCoreNLP('http://localhost:9000')

input_query = "When will my OPT start processing?"
input_tokens = nltk.tokenize.word_tokenize(input_query)

tags_mapping = defaultdict(lambda: '')

tags_mapping['V'] = 'v'
tags_mapping['J'] = 'a'
tags_mapping['N'] = 'n'

##tags_mapping = {'V':'v','J':'a','N':'n','P':'n','M':'v','W':'v','D':'',':':'','I':'','C':''}

def get_text(filename):
    filename = filename.replace("json","txt")
    text = open(os.getcwd()+"/corpus/"+filename, encoding='utf-8').read()
    return text

def return_sent_tokenize(text):
    return nltk.sent_tokenize(text)

def return_word_tokenize(text):
    return nltk.word_tokenize(text)

def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in words if not w in stop_words]
##    print(filtered_sentence)
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
        print(output['sentences'][0]['basicDependencies'])


        # parse_tree_string.append([output['sentences'][0]['basicDependencies'][0]['dep'],])
        for parse_dict in output['sentences'][0]['basicDependencies']:
            for key, value in parse_dict.items():
                if key == 'dep':
                    parse_tree_string.append((key, value))
                if key == 'dependentGloss':
                    parse_tree_string.append((key, value))

    # print("parse_tree_string: "+str(parse_tree_string))
    # parse_tree_string = set(parse_tree_string)
    # parse_tree_string = list(parse_tree_string)


        # parse_tree_string += output['sentences'][0]['parse']

    return parse_tree_string

def extract_hypernyms(words):

    hypernyms_list_of_all_words = []

    for word in words:
##        print(nltk.tag.pos_tag([word])[0][1])
##        print("nltk.tag.pos_tag([word])[0][1] \t"+tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
##            print("\nSense: "+str(s))
            hypernyms_collection = s.hypernyms()
            for h in hypernyms_collection:
                hypernyms_list_of_all_words.append(h.name().split(".")[0])
##                print(h.name().split(".")[0])
##                time.sleep(0.5)
##        print("\nEnd of word\n")

    hypernyms_list_of_all_words = set(hypernyms_list_of_all_words)

    hypernyms_list_of_all_words = list(hypernyms_list_of_all_words)

    return hypernyms_list_of_all_words


def extract_hyponyms(words):

    hyponyms_list_of_all_words = []


    for word in words:
##        print("nltk.tag.pos_tag([word])[0][1] \t"+tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
##            print("\nSense: "+str(s))
            hyponyms_collection = s.hyponyms()
            for h in hyponyms_collection:
                hyponyms_list_of_all_words.append(h.name().split(".")[0])
##                print(h.name().split(".")[0])
##                time.sleep(0.5)
##        print("\nEnd of word\n")

    hyponyms_list_of_all_words = set(hyponyms_list_of_all_words)

    hyponyms_list_of_all_words = list(hyponyms_list_of_all_words)

    return hyponyms_list_of_all_words


def extract_meronyms(words):

    meronyms_list_of_all_words = []

    for word in words:
##        print("nltk.tag.pos_tag([word])[0][1] \t"+tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
##            print("\nSense: "+str(s))
            meronyms_collection = s.part_meronyms()
            meronyms_collection += s.substance_meronyms()
            meronyms_collection += s.member_meronyms()

            for h in meronyms_collection:
                meronyms_list_of_all_words.append(h.name().split(".")[0])
##                print(h.name().split(".")[0])
##                time.sleep(0.5)
##        print("\nEnd of word\n")

    meronyms_list_of_all_words = set(meronyms_list_of_all_words)

    meronyms_list_of_all_words = list(meronyms_list_of_all_words)

    return meronyms_list_of_all_words

def extract_holonyms(words):

    holonyms_list_of_all_words = []

    for word in words:
##        print("nltk.tag.pos_tag([word])[0][1] \t"+tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
##            print("\nSense: "+str(s))
            holonyms_collection = s.part_holonyms()
            holonyms_collection += s.substance_holonyms()
            holonyms_collection += s.member_holonyms()

            for h in holonyms_collection:
                holonyms_list_of_all_words.append(h.name().split(".")[0])
##                print(h.name().split(".")[0])
##                time.sleep(0.5)
##        print("\nEnd of word\n")

    holonyms_list_of_all_words = set(holonyms_list_of_all_words)

    holonyms_list_of_all_words = list(holonyms_list_of_all_words)

    return holonyms_list_of_all_words


def extract_synonyms(words):

    synonyms_list_of_all_words = []

    for word in words:
##        print(nltk.tag.pos_tag([word])[0][1])
##        print("nltk.tag.pos_tag([word])[0][1] \t"+tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        senses = wordnet.synsets(word,pos=tags_mapping[nltk.tag.pos_tag([word])[0][1][0]])
        for s in senses:
            synonyms_list_of_all_words += s.lemma_names()
##            print(synonyms_list_of_all_words)
##            time.sleep(0.5)
##
##        print("\nEnd of word\n")

    synonyms_list_of_all_words = set(synonyms_list_of_all_words)

    synonyms_list_of_all_words = list(synonyms_list_of_all_words)

    return synonyms_list_of_all_words


def find_documents(query):

    content = query

    old_content = content

    sentences = return_sent_tokenize(content)

    words = return_word_tokenize(content)

    words_without_stop_words = remove_stop_words(words)

    words_with_stemming = stemming(words_without_stop_words)

    words_with_lemmatization = lemmatization(words_without_stop_words)

    words_with_pos_tags = pos_tags(words_without_stop_words)

    parse_tree_string = parse_tree(sentences)

    # print("parse_tree_string_input: " + str(parse_tree_string))

    hypernyms_list = extract_hypernyms(words_without_stop_words)

    hyponyms_list = extract_hyponyms(words_without_stop_words)

    meronyms_list = extract_meronyms(words_without_stop_words)

    holonyms_list = extract_holonyms(words_without_stop_words)

    synonyms_list = extract_synonyms(words_without_stop_words)

    # file_write = open('Task3Output/inputQuestion_outputTask3JSON.json','w')

    # print('Filename: '+str(filename))

    input_data = defaultdict()

    input_question = re.findall(r'.*\?', old_content)[0]

    input_answer = old_content.replace(re.findall(r'.*\?', old_content)[0],"")

    input_sentence_tokenizer = sentences

    input_words_tokenizer = words

    input_words_without_stop_words = words_without_stop_words

    input_words_with_stemming = words_with_stemming

    input_words_with_lemmatization = words_with_lemmatization

    input_words_with_pos_tags = words_with_pos_tags

    # print("input_words_with_pos_tags: "+str(input_words_with_pos_tags))

    input_parse_tree_string = parse_tree_string

    input_hypernyms_list = hypernyms_list

    input_hyponyms_list = hyponyms_list

    input_meronyms_list = meronyms_list

    input_holonyms_list = holonyms_list

    input_synonyms_list = synonyms_list

    #
    #
    # features_dictionary_for_input['question'] = re.findall(r'.*\?', old_content)[0]
    #
    # features_dictionary_for_input['answer'] = old_content.replace(re.findall(r'.*\?', old_content)[0],"")
    #
    # features_dictionary_for_input['sentence_tokenizer'] = sentences
    #
    # features_dictionary_for_input['words_tokenizer'] = words
    #
    # features_dictionary_for_input['words_without_stop_words'] = words_without_stop_words
    #
    # features_dictionary_for_input['words_with_stemming'] = words_with_stemming
    #
    # features_dictionary_for_input['words_with_lemmatization'] = words_with_lemmatization
    #
    # features_dictionary_for_input['words_with_pos_tags'] = words_with_pos_tags
    #
    # features_dictionary_for_input['parse_tree_string'] = parse_tree_string
    #
    # features_dictionary_for_input['hypernyms_list'] = hypernyms_list
    #
    # features_dictionary_for_input['hyponyms_list'] = hyponyms_list
    #
    # features_dictionary_for_input['meronyms_list'] = meronyms_list
    #
    # features_dictionary_for_input['holonyms_list'] = holonyms_list
    #
    # features_dictionary_for_input['synonyms_list'] = synonyms_list

    # file_write.write(json.dumps(input_data))

    # file_write.close()

    result_dict = {}

    # print("os.getcwd() "+str(os.getcwd()))
    #
    # os.chdir(os.getcwd()+"/CorpusFilesWithFeatures/")

    score_dict = {}

    for filename in tqdm(os.listdir(os.getcwd()+'/CorpusFilesWithFeatures/')):

        if filename.endswith(".json"):

            # print("filename: "+filename)

            match_num = {}

            value = 0.0

            # print(filename)

            content = open(os.getcwd()+'/CorpusFilesWithFeatures/'+filename)

            data = json.load(content)
            # print(file)

            question = data["question"]
            answer = data["answer"]
            sentence_tokenizer = data["sentence_tokenizer"]
            words_tokenizer = data["words_tokenizer"]
            words_without_stop_words = data["words_without_stop_words"]
            words_with_stemming = data["words_with_stemming"]
            words_with_lemmatization = data["words_with_lemmatization"]
            words_with_pos_tags = data["words_with_pos_tags"]
            parse_tree_string = data["parse_tree_string"]
            hypernyms_list = data["hypernyms_list"]
            hyponyms_list = data["hyponyms_list"]
            meronyms_list = data["meronyms_list"]
            holonyms_list = data["holonyms_list"]
            synonyms_list = data["synonyms_list"]




            match_num_sentence_tokenizer = set(sentence_tokenizer) & set(input_sentence_tokenizer)
            value += 10*len(match_num_sentence_tokenizer)/(len(input_sentence_tokenizer)+0.01)
            match_num["sentence_tokenizer"] = 10*len(match_num_sentence_tokenizer)/(len(input_sentence_tokenizer)+0.01)


            match_num_words_tokenizer = set(words_tokenizer) & set(input_words_tokenizer)
            value += 10*len(match_num_words_tokenizer)/(len(input_words_tokenizer)+0.01)
            match_num["words_tokenizer"] = 10*len(match_num_words_tokenizer)/(len(input_words_tokenizer)+0.01)

            match_num_without_stop_words = set(words_without_stop_words) & set(input_words_without_stop_words)
            value += 10*len(match_num_without_stop_words)/(len(input_words_without_stop_words)+0.01)
            match_num["stop_words"] = 10*len(match_num_without_stop_words)/(len(input_words_without_stop_words)+0.01)

            match_num_words_with_stemming = set(words_with_stemming) & set(input_words_with_stemming)
            value += 10*len(match_num_words_with_stemming)/(len(input_words_with_stemming)+0.01)
            match_num["stemming"] = 10*len(match_num_words_with_stemming)/(len(input_words_with_stemming)+0.01)


            match_num_words_with_lemmatization = set(words_with_lemmatization) & set(input_words_with_lemmatization)
            value += 10*len(match_num_words_with_lemmatization)/(len(input_words_with_lemmatization)+0.01)
            match_num["lemmatization"] = 10*len(match_num_words_with_lemmatization)/(len(input_words_with_lemmatization)+0.01)

            # print("words_with_pos_tags: "+str(words_with_pos_tags))
            # print("\n\ninput_words_with_pos_tags: "+str(input_words_with_pos_tags))

            words_with_pos_tags = [tuple(l) for l in (words_with_pos_tags)]

            match_num_words_with_pos_tags = set(words_with_pos_tags) & set(input_words_with_pos_tags)
            value += 7*len(match_num_words_with_pos_tags)/(len(input_words_with_pos_tags)+0.01)
            match_num["pos_tags"] = 7*len(match_num_words_with_pos_tags)/(len(input_words_with_pos_tags)+0.01)

            parse_tree_string = [tuple(l) for l in (parse_tree_string)]

            # print("parse_tree_string: "+str(parse_tree_string))
            # print("input_parse_tree_string: "+str(input_parse_tree_string))


            match_num_words_with_parse_tree_string = set(parse_tree_string) & set(input_parse_tree_string)
            value += 3*len(match_num_words_with_parse_tree_string)/(len(input_parse_tree_string)+0.01)
            match_num["parse_tree_string"] = 3*len(match_num_words_with_parse_tree_string)/(len(input_parse_tree_string)+0.01)




            match_num_words_with_hypernyms_list = set(hypernyms_list) & set(input_hypernyms_list)
            value += 6*len(match_num_words_with_hypernyms_list)/(len(input_hypernyms_list)+0.01)
            match_num["hypernyms_list"] = 6*len(match_num_words_with_hypernyms_list)/(len(input_hypernyms_list)+0.01)


            match_num_words_with_hyponyms_list = set(hyponyms_list) & set(input_hyponyms_list)
            value += 6*len(match_num_words_with_hyponyms_list)/(len(input_hyponyms_list)+0.01)
            match_num["hyponyms_list"] = 6*len(match_num_words_with_hyponyms_list)/(len(input_hyponyms_list)+0.01)

            match_num_words_with_meronyms_list = set(meronyms_list) & set(input_meronyms_list)
            value += 3*len(match_num_words_with_meronyms_list)/(len(input_meronyms_list)+0.01)
            match_num["meronyms_list"] = 3*len(match_num_words_with_meronyms_list)/(len(input_meronyms_list)+0.01)


            match_num_words_with_holonyms_list = set(holonyms_list) & set(input_holonyms_list)
            value += 3*len(match_num_words_with_holonyms_list)/(len(input_holonyms_list)+0.01)
            match_num["holonyms_list"] = 3*len(match_num_words_with_holonyms_list)/(len(input_holonyms_list)+0.01)


            match_num_words_with_synonyms_list = set(synonyms_list) & set(input_synonyms_list)
            value += 8*len(match_num_words_with_synonyms_list)/(len(input_synonyms_list)+0.01)
            match_num["synonyms_list"] = 8*len(match_num_words_with_synonyms_list)/(len(input_synonyms_list)+0.01)

            print(json.dumps(match_num, indent=4, sort_keys=True))

            score_dict[filename] = value


    filename_with_score_sorted = sorted(score_dict, key=lambda k: (score_dict[k]), reverse=True)

    filename_with_score_sorted = filename_with_score_sorted[0:10]

    for filename in filename_with_score_sorted:
        print(filename)

    for key, value in score_dict.items():
        print("key: "+str(key)+"\tvalue: "+str(value))


    top_ten_documents = defaultdict()

    i = 1
    for value in filename_with_score_sorted:
            value = value.replace('_outputTask3JSON','')
            top_ten_documents[i] = value
            i = i+1

    print("top_ten_documents"+str(top_ten_documents))
    return top_ten_documents



#
#
# for filename in tqdm(os.listdir(os.getcwd())):
#         if '.txt' in filename:
# ##                print(filename)
#                 # content = open(filename, encoding='utf-8').read()
#
#                 content = "When will my OPT start processing?"
#
#                 old_content = content
#
# ##                content = content.replace(".","").replace(",","").replace("?","").replace(':','')
#
#                 sentences = return_sent_tokenize(content)
#
#                 words = return_word_tokenize(content)
#
#                 words_without_stop_words = remove_stop_words(words)
#
#                 words_with_stemming = stemming(words_without_stop_words)
#
#                 words_with_lemmatization = lemmatization(words_without_stop_words)
#
#                 words_with_pos_tags = pos_tags(words_without_stop_words)
#
#                 parse_tree_string = parse_tree(sentences)
#
#                 hypernyms_list = extract_hypernyms(words_without_stop_words)
#
#                 hyponyms_list = extract_hyponyms(words_without_stop_words)
#
#                 meronyms_list = extract_meronyms(words_without_stop_words)
#
#                 holonyms_list = extract_holonyms(words_without_stop_words)
#
#                 synonyms_list = extract_synonyms(words_without_stop_words)
#
#                 file_write = open('Task3Output/'+filename.split('.')[0] + "_outputTask3JSON.json",'w')
#
#                 print('Filename: '+str(filename))
#
#                 features_dictionary = defaultdict()
#
#                 features_dictionary['question'] = re.findall(r'.*\?', old_content)[0]
#
#                 features_dictionary['answer'] = old_content.replace(re.findall(r'.*\?', old_content)[0],"")
#
#                 features_dictionary['sentence_tokenizer'] = sentences
#
#                 features_dictionary['words_tokenizer'] = words
#
#                 features_dictionary['words_without_stop_words'] = words_without_stop_words
#
#                 features_dictionary['words_with_stemming'] = words_with_stemming
#
#                 features_dictionary['words_with_lemmatization'] = words_with_lemmatization
#
#                 features_dictionary['words_with_pos_tags'] = words_with_pos_tags
#
#                 features_dictionary['parse_tree_string'] = parse_tree_string
#
#                 features_dictionary['hypernyms_list'] = hypernyms_list
#
#                 features_dictionary['hyponyms_list'] = hyponyms_list
#
#                 features_dictionary['meronyms_list'] = meronyms_list
#
#                 features_dictionary['holonyms_list'] = holonyms_list
#
#                 features_dictionary['synonyms_list'] = synonyms_list
#
#                 file_write.write(json.dumps(features_dictionary))
#
#
#
#
#
#                 # file_write.write("Corpus Question: "+re.findall(r'.*\?', old_content)[0])
#                 # file_write.write("\n\nCorpus Answer: "+(old_content.replace(re.findall(r'.*\?', old_content)[0],"")).encode('ascii', 'ignore').decode('ascii'))
#                 # file_write.write("\n\nSentence Tokenizer: "+ str(sentences))
#                 # file_write.write("\n\nWords Tokenizer: "+ str(words))
#                 # file_write.write("\n\nwords_without_stop_words: "+ str(words_without_stop_words))
#                 # file_write.write("\n\nwords_with_stemming: "+ str(words_with_stemming))
#                 # file_write.write("\n\nwords_with_lemmatization: "+ str(words_with_lemmatization))
#                 # file_write.write("\n\nwords_with_pos_tags: "+ str(words_with_pos_tags))
#                 # file_write.write("\n\nparse_tree_string: "+ str(parse_tree_string))
#                 # file_write.write("\n\nhypernyms_list: "+ str(hypernyms_list))
#                 # file_write.write("\n\nhyponyms_list: "+ str(hyponyms_list))
#                 # file_write.write("\n\nmeronyms_list: "+ str(meronyms_list))
#                 # file_write.write("\n\nholonyms_list: "+ str(holonyms_list))
#                 # file_write.write("\n\nsynonyms_list: "+ str(synonyms_list))
#                 file_write.close()
#
#
# ##
# ##                print(words_with_pos_tags)
# ##                print(synonyms_list)
# ##
