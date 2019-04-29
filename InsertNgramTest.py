# -*- coding: utf-8 -*-
import Mongodb as mongo
from os import listdir
import document2json
import pdb
from InsertMongo import convert_text, list_files

def insertCorpus(directory):
    files = list_files(directory, "txt")
    documents = []
    for f in files:
        try:
            content = ""
            file = open(directory + '/' + f, 'r+')
            content = file.read()
            if (content == ""):
                continue
            content = convert_text(content)
            document = document2json.document_json(title=f, content=content, lang="english")
            documents.append(document)
            file.close()
        except IOError as e:
            print("Reading file %s failed: %s" % (f, e))
        except UnicodeDecodeError as e:
            print("Some error occurred decoding file %s: %s" % (f, e))
    mongo.bulk_insert("ngramTest", documents)


if __name__ == '__main__':
    directoryTestNgram = '/home/tmc/Documents/NLP/cross_language/Test/English'
    insertCorpus(directoryTestNgram)