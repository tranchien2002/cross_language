# -*- coding: utf-8 -*-
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import Mongodb as mongo
from bson.objectid import ObjectId
from document2json import ngram_json
from InsertMongo import convert_text
import pdb
import time
import os
import string
import _pickle as cPickle
from bson.objectid import ObjectId
docs_col = mongo.get_colection("documents")
test_col = mongo.get_colection("ngramTest")


def ngrams_token(document, n):
  input = document.split(' ')
  output = []
  setNgram = {}
  for i in range(len(input)-n+1):
    g = ' '.join(input[i:i+n])
    setNgram.setdefault(g, 0)
    setNgram[g] += 1
  for key in setNgram.keys():
      output.append(key);
  return output

def load_lsh():
    if(os.path.isfile('pickle_ngram.txt')):
        inf = open('pickle_ngram.txt', 'rb')
        forest = cPickle.load(inf)
    else:
        forest = store_lsh()
    return forest

def query_candidates(doc, topn):
    lsh = load_lsh()
    minhash = MinHash(num_perm=128)
    content = convert_text(doc['content'])
    ngram = ngrams_token(remove_punctuation(content), 3)
    for gram in ngram:
        minhash.update(gram.encode('utf-8'))
    result = lsh.query(minhash, topn)

    print(doc['title'])
    if result:
        for item in result:
            doc = docs_col.find_one({"_id": ObjectId(str(item))})
            print(doc['title'])
    print("=====================")
    return result

def store_lsh():
    forest = MinHashLSHForest(num_perm=128)
    documents_en = docs_col.find({"lang": 'english'})
    for item in documents_en:
        minhash = MinHash(num_perm=128)
        ngrams = ngrams_token(remove_punctuation(item['content']), 3)
        for ngram in ngrams:
            minhash.update(ngram.encode("utf-8"))
        forest.add(str(item["_id"]), minhash)
    forest.index()
    ouf = open('pickle_ngram.txt', 'wb')
    cPickle.dump(forest, ouf)
    ouf.close()
    return forest

def remove_punctuation(text):
    return ' '.join(word.strip(string.punctuation) for word in text.split())

if __name__ == '__main__':
    doc = test_col.find({})
    for item in doc:
        result = query_candidates(item, 3)