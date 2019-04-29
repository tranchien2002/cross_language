# -*- coding: utf-8 -*-
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import Mongodb as mongo
from bson.objectid import ObjectId
from document2json import pickle_json, lsh_json, document_json
from KeywordInput import get_top_n_words_tf
import pdb
import time
docs_col = mongo.get_colection("documents")

def get_topn_similarity_documents_lsh(keywords, n = 3):
    lsh = MinHashLSH(threshold=0.1, num_perm=128)
    documents_en = docs_col.find({"lang": 'english'})
    documents_min = [lsh_json(str(item["_id"]), item["keyword"]) for item in documents_en]
    for item in documents_min:
        minhash = MinHash(num_perm=128)
        list_keyword = item["keyword"].split(",")
        for k in list_keyword:
            minhash.update(k.encode("utf-8"))
        lsh.insert(str(item["id"]), minhash)

    min = MinHash(num_perm=128)
    keywords = keywords.split(",")
    for k in keywords:
        # print(k)
        min.update(k.encode("utf-8"))
    result = lsh.query(min)
    list_docs = []
    if result:
        for item in result:
            doc = docs_col.find_one({"_id": ObjectId(str(item))})
            doc.pop('_id', None)
            list_docs.append(doc)
    print(list_docs)
    return list_docs

def query_candidates(doc, topn):
    min = MinHash(num_perm=128)
    keyword = doc['keyword'].split(",")
    # keyword = get_top_n_words_tf(doc['content'])
    for k in keyword:
        min.update(k.encode('utf8'))

    result = forest.query(min, topn)
    print(doc['title'])
    filename = "result_minHashLSHforest.txt"
    myfile = open(filename, 'a+')
    myfile.write(doc['title'] + '\n')
    if result:
        for item in result:
            doc = docs_col.find_one({"_id": ObjectId(str(item))})
            print(doc['title'])
            myfile.write(doc['title'] + '\n')
    myfile.write("================" + '\n')
    print("=====================")

if __name__ == '__main__':
    forest = MinHashLSHForest(num_perm=128)
    documents_en = docs_col.find({"lang": 'english'})
    for item in documents_en:
        minhash = MinHash(num_perm=128)
        list_keyword = item["keyword"].split(",")
        for k in list_keyword:
            minhash.update(k.encode("utf-8"))
        forest.add(str(item["_id"]), minhash)
    forest.index()

    documents_vi = docs_col.find({"lang": 'vietnamese'})
    documents = [document_json(str(item["title"]), item["content"], keyword=item["keyword"]) for item in documents_vi]
    start_time = time.time()
    for doc in documents:
        # pdb.set_trace()
        query_candidates(doc, 5)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
