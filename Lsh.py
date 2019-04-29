# -*- coding: utf-8 -*-
import database as mydb
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import pdb
from Translator import translate, translate_yandex
from Article import Article
import time
# Create MinHash objects





def query_candidates(doc):
    min = MinHash(num_perm=128)
    keyword = doc.keyword.split(",")
    for k in keyword:
        time.sleep(2)
        # print(k)
        trans_text = translate_yandex(str(k), src="vi", dest="en").encode("utf-8")
        print(trans_text)
        min.update(trans_text)
    # result = forest.query(min, 3)
    result = lsh.query(min)
    result = ",".join(result)
    if not result:
        print(doc.title)
        print("----------------------------------------------")
        print("Not found")
        print("\n")
    else:
        docs = mydb.execute_query("SELECT id, keyword, title FROM english WHERE id IN (" + result + ")")
        titles = [Article(id=item[0], keyword=item[1], title=item[2]) for item in docs]
        print(doc.title)
        print("----------------------------------------------")
        for i in titles:
            print(i.title)
        print("\n")

if __name__ == '__main__':

    # forest = MinHashLSHForest(num_perm=128)
    lsh = MinHashLSH(threshold=0.1, num_perm=128)
    articles_en = mydb.execute_query("SELECT id, keyword, title FROM english")
    keywords_en = [Article(id=item[0], keyword=item[1], content=item[2]) for item in articles_en]
    for item in keywords_en:
        minhash = MinHash(num_perm=128)
        list_keyword = item.keyword.split(",")
        for k in list_keyword:
            minhash.update(k.encode("utf-8"))
        lsh.insert(str(item.id), minhash)
    #     forest.add(str(item.id), minhash)
    # forest.index()
    # lsh = MinHashLSH(num_perm=128, threshold=0.1, storage_config = {
    #     "type": "redis",
    #     "basename": b"docs_tech",
    #     "redis": {"host": "localhost", "port": 6379}
    # })c


    docs = mydb.execute_query("SELECT id, keyword, title FROM vietnamese")
    docs_vn = [Article(id = item[0], keyword = item[1], title = item[2]) for item in docs]

    for doc in docs_vn:
        query_candidates(doc)






# keyword = docs_vn[0].keyword.split(",")
# min = MinHash(num_perm=128)
# for k in keyword:
#     min.update(translate(str(k), src="vi", dest="en").encode("utf-8"))
# result = forest.query(min, 3)
#
# result = ",".join(result)
#
# articles = mydb.execute_query("SELECT id, keyword, title FROM english WHERE id IN (" + result +  ")")
# contents = [Article(id = item[0], keyword = item[1], content = item[2]) for item in articles]
# print(docs_vn[0].content)
# print("----------------------------------------------")
# for i in contents:
#     print(i.content)

