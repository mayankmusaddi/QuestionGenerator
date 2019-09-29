
import re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
# nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer

def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text

def load_data(folder_path):
    dataset = []
    for i in range(1,11):
        path = folder_path+str(i)+".txt"
        text = read_data(path)
        dataset.append(text)
    return dataset
    # print(text)
dataset = load_data("physics_data/")

# ##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))

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

corpus = create_corpus(dataset)

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
    fig.savefig("word1.png", dpi=900)

#Function for sorting tf_idf in descending order
from scipy.sparse import coo_matrix
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

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(1,3))
X=cv.fit_transform(corpus) 
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(X)# get feature names
feature_names=cv.get_feature_names()

def create_keywords(doc):
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items,1000)
    return keywords

# nltk.download('punkt')
from textblob import TextBlob

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

    final = ""
    for i in range(num):
        print(imp[i][1])
        final +=imp[i][1]+"\n"
    return final

# fetch document for which keywords needs to be extracted
# doc=corpus[9]
out = final_out(9,100)
print(out)