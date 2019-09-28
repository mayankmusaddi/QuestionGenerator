import re
import random
import sys
import os.path
from os import path
import nltk
from textblob import TextBlob

debug_flag = False


def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text


def create_blank(word, sentence):
    buff = re.compile(re.escape(word), re.IGNORECASE)
    return buff.sub('_______________', sentence)

def remove_word(sentence,poss):

    words = None

    if 'NNP' in poss:
        words = poss['NNP'] 
        ## Will output this in the json file. All the words which can be replaced and the sentences.
    elif 'NN' in poss:
        words = poss['NN']
    else:
        ## Skip the sentences which do not have a proper noun or a noun.
        ## Will have to add co-referencing for these sentences.
        # print("No instance of NN and NNP-2")
        return(None,sentence,None)
    
    if len(words) > 0:
        word = random.choice(words)
        replaced = create_blank(word,sentence)
        return (word,sentence,replaced)
    else:
        # print("No instance of NN and NNP-2")
        pass
    
def process(text):
    blob_text = TextBlob(text)

    if debug_flag == True:
        print(blob_text)
        print(blob_text.tags)

    sposs = {}

    for sentence in blob_text.sentences:

        # Grouping the words based on the pos
        # creating a dict with keys as part of speech and the values as the words with that pos
        poss = {}
        sposs[sentence.string] = poss

        for t in sentence.tags:
            tag = t[1]
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(t[0])
        
    # print(sposs)
    return sposs


def main():
    sposs = process(text)
    print(sposs)
    # for sentence in sposs.keys():
    #     poss = sposs[sentence]
    
    # (word,original,replaced) = remove_word(sentence,poss)

    # if replaced is None:
    #     pass
    # else:
    #     print(replaced)
    #     print ("\n===============")
    #     print(word)
    #     print ("===============")
    #     print("\n")
        

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
            text = read_data(file_path)
            # print(text)
            main()
            
