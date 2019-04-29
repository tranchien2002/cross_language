# -*- coding: utf-8 -*-
import database as mydb
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import pdb
from Translator import translate
from Article import Article
# Create MinHash objects




lsh = MinHashLSH(threshold=0.1, num_perm=128, storage_config = {
    "type": "redis",
    "basename": b"docs_tech",
    "redis": {"host": "localhost", "port": 6379}
})
lsh = MinHashLSH(threshold=0.2, num_perm=128)
articles_en = mydb.execute_query("SELECT id, keyword, title FROM english")
keywords_en= [Article(id = item[0], keyword = item[1], content = item[2]) for item in articles_en]
for item in keywords_en:
    minhash = MinHash(num_perm=128)
    list_keyword = item.keyword.split(",")
    for k in list_keyword:
        minhash.update(k.encode("utf-8"))
    lsh.insert(str(item.id), minhash)
    # forest.add(str(item.id), minhash)
# forest.index()