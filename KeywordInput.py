# -*- coding: utf-8 -*-
import Mongodb as mongo
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pdb
import json
from bson.objectid import ObjectId
from Translator import translate, translate_yandex
from pyvi import ViTokenizer
from KeywordMongo import convert_text
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

if __name__ == '__main__':
    articles_vi = mongo_col.find({"lang": 'vietnamese'})
    # pdb.set_trace()
    words = ViTokenizer.tokenize(convert_text(articles_vi[2]['content']))
    test = get_top_n_words_tf(words, 15)
    # pdb.set_trace()
    print(test[0])