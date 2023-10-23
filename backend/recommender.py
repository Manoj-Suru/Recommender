import numpy as np
import pandas as pd

#movies = pd.read_csv('../dataset/movie.csv')
movies = pd.read_csv('../dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('../dataset/tmdb_5000_credits.csv')

movies = movies.merge(credits,on="title")

#genres,id(posters),keywords,title(in english),overview,cast&crew(actor based)
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

import ast
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert3(obj):
    counter = 0
    L = []
    for i in ast.literal_eval(obj):
        if(counter != 3): 
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert3)

def director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if(i['job'] == 'Director'): 
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(director)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

#remove spaces in genres,keywords,cast,crew for full name match
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords']+movies['cast'] + movies['crew']

new_df = movies[['movie_id','title','tags']]

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
#lowercase all
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

#text vectorization (eg: bag of words, tfidf, word2vec)
#stop words don't contribute in meaning (eg: is, to)
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

#cosine distance
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

def recommend(movie):
    idx = new_df[new_df['title'] == movie].index[0]
    distances = similarity[idx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(new_df.iloc[i[0]].title)
