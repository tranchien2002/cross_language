# -*- coding: utf-8 -*-
import Mongodb as mongo
from sklearn.feature_extraction.text import CountVectorizer
from Article import Article
from sklearn.feature_extraction.text import TfidfTransformer
import pdb
import json
from bson.objectid import ObjectId
from Translator import translate, translate_yandex
from pyvi import ViTokenizer
mongo_col = mongo.get_colection("documents")

def get_top_n_words_tf(doc, n=None):
    with open("stopwords_vn.txt") as f:
        content = f.readlines()
    stopwords = frozenset([x.strip() for x in content])
    words = ViTokenizer.tokenize(convert_text(doc))
    vec = CountVectorizer(stop_words=stopwords).fit([words])
    bag_of_words = vec.transform([words])
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1],
                       reverse=True)
    topn = words_freq[:n]
    topn = [item[0] for item in topn]
    return topn

def convert_text(text):
  converted = text.replace('“', '')
  converted = converted.replace('”', '')
  converted = converted.replace("’", "")
  converted = converted.replace("'", "")
  converted = converted.replace('"', '')
  return converted.lower()

def counter(lang, word = False):
    docs = mongo_col.find({"lang": lang})

    if(word):
        contents = [item['words'] for item in docs]
    else:
        contents = [item['content'] for item in docs]
    cv = CountVectorizer(stop_words = get_stopwords(lang))
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

def extract_topn_from_vector(doc, lang , topn=15, word = False):
    """get the feature names and tf-idf score of top n items"""
    cv, word_count_vector = counter(lang, word)
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

def counter_new_vi_doc(content):
    documents = mongo_col.find({"lang": "vietnamese"})
    content = ViTokenizer.tokenize(convert_text(content))
    contents = [item['words'] for item in documents]
    contents.append(content)
    cv = CountVectorizer(stop_words=get_stopwords("vietnamese"))
    return cv, cv.fit_transform(contents)

def extract_topn_new_vi_doc(content, topn = 10):
    cv, word_count_vector = counter_new_vi_doc(content)
    feature_names = cv.get_feature_names()
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    tf_idf_vector = tfidf_transformer.transform(cv.transform([content]))

    # use only topn items from vector
    sorted_items = sort_coo(tf_idf_vector.tocoo())[:topn]

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

def update_keyword(id, new_keyword, lang = ""):
    if(lang == "vietnamese"):
        # translate keyword & get first word if getting more than a word
        new_keyword = [translate_yandex(item, src="vi", dest="en").split(" ")[0] for item in new_keyword]
    new_keyword = ','.join(new_keyword)
    mongo_col.update({'_id': ObjectId(id)}, {'$set' : {'keyword_tf': new_keyword}})

def trans_keyword(new_keyword):
    new_keyword = [translate_yandex(item, src="vi", dest="en").split(" ")[0] for item in new_keyword]
    new_keyword = ','.join(new_keyword)
    return new_keyword

if __name__ == '__main__':
    # articles_en = mongo_col.find({"lang": 'english'})
    docs_vi = mongo_col.find({"lang": 'vietnamese'})
    # for a in articles_en:
    #     update_keyword(str(a['_id']), extract_topn_from_vector(a['content'], "english", 15))
    for a in docs_vi:
        # update_keyword(str(a['_id']), get_top_n_words_tf(a['words'], "vietnamese", 15, word=True), lang="vietnamese")
        update_keyword(str(a['_id']), get_top_n_words_tf(a['content'], 15), lang="vietnamese")



