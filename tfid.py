
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer

from scipy.sparse import coo_matrix

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
nltk.download('punkt')
from textblob import TextBlob
import os
import sys

def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text

def load_data(folder_path):
    dataset = []
    fnames = []
    for file in os.listdir(folder_path):
        if file.endswith("_final.txt"):
            filename = os.path.join(folder_path, file)
            fnames.append(filename)
            text = read_data(filename)
            dataset.append(text)
    return dataset,fnames

def create_corpus(dataset):
    corpus = []
    for text in dataset:

        #Remove punctuations
        text = re.sub('[^a-zA-Z]', ' ',text)

        #Convert to lowercase
        text = text.lower()

        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        ##Convert to list from string
        text = text.split()

        ##Stemming
        ps=PorterStemmer()    #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in  
                stop_words] 
        text = " ".join(text)
        corpus.append(text)
    return corpus

def create_wordcloud(text):
    from os import path
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    import matplotlib.pyplot as plt
    # % matplotlib inline
    wordcloud = WordCloud(
                              background_color='white',
                              stopwords=stop_words,
                              max_words=100,
                              max_font_size=50, 
                              random_state=42
                             ).generate(str(text))
    print(wordcloud)
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    fig.savefig("word1.png", dpi=300)


#Function for sorting tf_idf in descending order

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def create_keywords(doc):
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items,1000)
    return keywords

def score_sentence(text,keywords):
    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ',text)
    #Convert to lowercase
    text = text.lower()
    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    ##Convert to list from string
    text = text.split()
    ##Stemming
    ps=PorterStemmer()    #Lemmatisation
    lem = WordNetLemmatizer()

    score = 0
    for word in text:
        if not word in stop_words:
            wd = lem.lemmatize(word)
            if wd in keywords:
                score += keywords[wd]
    return score

def final_out(fileno,num):
    text = dataset[fileno]
    keywords = create_keywords(corpus[fileno])
    blob_text = TextBlob(text)
    imp = []
    for text in blob_text.sentences:
        score = score_sentence(str(text),keywords)
        imp.append([score,str(text)])
    imp.sort(reverse = True)

    n  = min(len(imp),num)
    final = ""
    for i in range(n):
        # print(imp[i][1])
        final +=imp[i][1]+"\n"
    return final

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please Enter the DirectoryPath")
        print("Usage: python3 tfid.py ''DirectoryPath''")
        sys.exit(1)
    else:
        command = sys.argv
        directorypath = sys.argv[1]
        dataset,fnames = load_data(directorypath)
        # print(dataset)
    
<<<<<<< HEAD
    # ##Creating a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words("english"))
    corpus = create_corpus(dataset)
    create_wordcloud(corpus[0])
    # print(corpus[0])
=======
        # ##Creating a list of stop words and adding custom stopwords
        stop_words = set(stopwords.words("english"))
        corpus = create_corpus(dataset)
        # print(corpus[0])
>>>>>>> 4f58cf0cc230bf00d183ce37ca9f4e53ba112cc1
    
        cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
        X=cv.fit_transform(corpus) 
        tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
        tfidf_transformer.fit(X)# get feature names
        feature_names=cv.get_feature_names()
    
        # fetch document for which keywords needs to be extracted
        # doc=corpus[9]
        # out = final_out(0,200)
        for i in range(len(fnames)):
            out = final_out(i,500)
            filename = fnames[i].replace("_final.txt", "_tfidf.txt")
            f = open(filename, "w")
            f.write(out)
            f.close()
    