# -*- coding: utf-8 -*-
import database as mydb
from sklearn.feature_extraction.text import CountVectorizer
from Article import Article
from sklearn.feature_extraction.text import TfidfTransformer
from Translator import translate
import pdb
import json

def counter(table, word = False):
    articles = mydb.execute_query("SELECT id, content, word, keyword FROM " + table)
    list_articles = [Article(item[0], item[1], item[2], item[3]) for item in articles]
    if(word):
        contents = [item.word for item in list_articles]
    else:
        contents = [item.content for item in list_articles]
    cv = CountVectorizer(stop_words = get_stopwords(table))
    return cv, cv.fit_transform(contents)

def get_stopwords(language):
    if(language == "vietnamese"):
        with open("stopwords_vn.txt") as f:
            content = f.readlines()
        stopwords = frozenset([x.strip() for x in content])
    elif(language == "english"):
        stopwords = "english"
    else:
        stopwords = "english"
    return stopwords

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(doc, table , topn=10, word = False):
    """get the feature names and tf-idf score of top n items"""
    cv, word_count_vector = counter(table, word)
    feature_names = cv.get_feature_names()
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

    # use only topn items from vector
    sorted_items=sort_coo(tf_idf_vector.tocoo())[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return feature_vals

def update_keyword(table, id, new_keyword):
    new_keyword = ",".join(new_keyword)
    mydb.update('UPDATE ' + table + ' SET keyword = "' + new_keyword + '" WHERE id = ' + id)

if __name__ == '__main__':
    articles = mydb.execute_query("SELECT id, content, word FROM english")
    list_articles = [Article(item[0], item[1], item[2]) for item in articles]
    contents = [item.content for item in list_articles]
    articles1 = mydb.execute_query("SELECT id, content, word FROM vietnamese")
    list_articles1 = [Article(item[0], item[1], item[2]) for item in articles1]
    contents1 = [item.word for item in list_articles1]
    # for a in list_articles:
    #     update_keyword("english", str(a.id), extract_topn_from_vector(a.content, "english", 15))
    for a in list_articles1:
        update_keyword("vietnamese", str(a.id), extract_topn_from_vector(a.word, "vietnamese", 15, word=True))