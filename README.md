# Question Generator

## FILE STRUCTURE
    
    bfq_ner.py : This is the main file which generates the fill in the blanks.
    pprocessing.py : Preprocesses the input data and feeds it to tfid.py
    tfid.py : Generates the most important sentences out of which bfq_ner.py will generate fill in the blanks.
    mcq.py : Generates the options for the given word.
    
## HOW TO RUN

```
python3 pprocessing.py 'foldername'
```

```
python3 tfid.py 'foldername'
```

```
python3 bfq_ner.py 'foldername'
```

The output of all the files goes into the 'foldername' directory.

## Major modules used
- NLTK
- Spacey
- gensim

All the requirements are mentioned in the requirements.txt file.

## Concepts
- Named Entity Recognition

## Repositories Referred
- https://github.com/cloudxlab/ml/blob/master/projects/autoquiz/auto_create_quiz.py.ipynb    
- https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
    
## Papers 
- http://www.ijcset.com/docs/IJCSET17-08-08-039.pdf
- https://aclweb.org/anthology/N10-1086

## Datasets used
- glove.6B.300d.word2vec.txt
- squad_dev-v1.1.json
- squad_train-v1.1.json

## Contributors:
- Mayank Mussaddi
- Parth Goyal
- Paryul Jain
- Aditya Morolia

### Developed as a part of Megathon'19 challenge, offered by Embibe [hosted at IIIT Hyderabad]