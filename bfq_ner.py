import re
import random
import sys
import os.path
from os import path
import nltk
from textblob import TextBlob
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import json                 
from gensim.models import KeyedVectors


debug_flag = 0

def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text

def create_blank(word, sentence):
    buff = re.compile(re.escape(word), re.IGNORECASE)
    return buff.sub('_______________', sentence)

# =================== main
def main():
    data_arr = []
    nlp = en_core_web_sm.load()
    text = read_data(file_path)
    processed_text = nlp(text)

    final_array = []
    for sentence in processed_text.sents:
        if len(sentence) > 5:

            if debug_flag == 1:
                print(len(sentence))
                print(sentence)
            
            words = []
            sentence_str = ''
            for token in sentence:
                sentence_str = sentence_str + ' ' + str(token.text)

        
            if len(sentence.ents) > 0:
                word = random.choice(sentence.ents).text

                for i in sentence.ents:
                    words.append(i.text)

                if debug_flag == 1:                
                    print(sentence_str)               
                    print ("\n===============")
                    print(sentence.ents)
                    print ("===============")
                    print("\n")

                dict = {"text": sentence_str, "fibs": words}
                final_array.append(dict)

    for i in final_array:
        print (i)

# ================ Most similar word for MCQ
# In[12]:
def most_similar_word(word):
    word_vec = KeyedVectors.load_word2vec_format('datasets/glove.6B.300d.word2vec.txt')
    ret = word_vec.most_similar(word)
    return word_vec

# =================
if __name__ == "__main__":
    command = ''
    if len(sys.argv) < 2:
        print("Please Enter a Filename")
        print("Usage: python3 bfq.py ''filename''")
        sys.exit(1)
    else:
        command = sys.argv
        filename = sys.argv[1]
        file_path = 'files/' + filename
        if (path.exists(file_path) == False):
            print("File Does Not Exist")
        else:
            main()