#!/usr/bin/env python
# coding: utf-8

# In[5]:


from gensim.models import KeyedVectors
import gensim.downloader as api


# In[12]:
def train():
    word_vec = KeyedVectors.load_word2vec_format('datasets/glove.6B.300d.word2vec.txt')
    return word_vec

word_vec = train()
word = 'centres'
ret = word_vec.most_similar(word)
print(ret)
