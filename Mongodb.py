from pymongo import MongoClient
import pdb
client = MongoClient('localhost', 27017)
db = client.test_15



def single_insert(colection, document):
    col = db[colection]
    col.insert_one(document)

def bulk_insert(colection, documents):
    col = db[colection]
    col.insert_many(documents)

def get_colection(colection):
    return db[colection]

def find_by_ids(colection, ids):
    col = db[colection]

