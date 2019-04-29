# -*- coding: utf-8 -*-
import Mongodb as mongo
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
from KeywordInput import get_top_n_words_tf
import time
from bson.objectid import ObjectId
docs_col = mongo.get_colection("documents")
test = mongo.get_colection("vnmeseTest")


def query_candidates(doc, topn):
    min = MinHash(num_perm=128)
    # keyword = doc['keyword'].split(",")
    keyword = get_top_n_words_tf(doc['content'], 15)
    for k in keyword:
        min.update(k.encode('utf8'))

    result = forest.query(min, topn)
    print(doc['title'])
    # filename = "result_minHashLSHforest.txt"
    # myfile = open(filename, 'a+')
    # myfile.write(doc['title'] + '\n')
    if result:
        for item in result:
            doc = docs_col.find_one({"_id": ObjectId(str(item))})
            print(doc['title'])
            # myfile.write(doc['title'] + '\n')
    # myfile.write("================" + '\n')
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
    start_time = time.time()
    for doc in documents_vi:
        # pdb.set_trace()
        query_candidates(doc, 5)
    elapsed_time = time.time() - start_time
    print(elapsed_time)