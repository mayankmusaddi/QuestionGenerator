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


debug_flag = 0

def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text

def create_blank(word, sentence):
    buff = re.compile(re.escape(word), re.IGNORECASE)
    return buff.sub('_______________', sentence)

def main():
    nlp = en_core_web_sm.load()
    text = read_data(file_path)
    processed_text = nlp(text)

    for sentence in processed_text.sents:
        if len(sentence) > 7:

            if debug_flag == 1:
                # print(len(sentence))
                print(sentence)

            # print(len(sentence.ents) , sentence)
            # print(sentence.ents)
            # print(type(str(sentence.text)))
            sentence_str = ''
            for token in sentence:
                sentence_str = sentence_str + ' ' + str(token.text)

            # print(sentence_str)
            # print(type(sentence_str))

            if len(sentence.ents) > 0:
                word = random.choice(sentence.ents).text
                # print(word)
                # print(type(word))
                # replaced = create_blank(word,sentence_str)

                print(sentence_str)               
                # print ("\n===============")
                # print(replaced)
                print ("\n===============")
                # print(word)
                print(sentence.ents)
                print ("===============")
                print("\n")
                





        

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