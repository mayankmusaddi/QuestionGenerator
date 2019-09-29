from gensim.models import KeyedVectors
import gensim.downloader as api

def train():
    word_vec = KeyedVectors.load_word2vec_format('datasets/glove.6B.300d.word2vec.txt')
    return word_vec


def getDistractor(word_vec,word):
    return word_vec.most_similar(word)

word_vec = train()
getDistractor(word_vec,'centres')