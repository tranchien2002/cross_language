# -*- coding: utf-8 -*-
import Mongodb as mongo
from sklearn.feature_extraction.text import TfidfVectorizer
from underthesea import word_tokenize
from pyvi import ViTokenizer
from os import listdir
import document2json
import pdb
import json

def convert_text(text):
  converted = text.replace('“', '')
  converted = converted.replace('”', '')
  converted = converted.replace("’", "")
  converted = converted.replace("'", "")
  converted = converted.replace('"', '')
  return converted.lower()

def list_files(directory, extension):
  return (f for f in listdir(directory) if f.endswith('.' + extension))

def insertCorpus(directory, word = False):
  files = list_files(directory, "txt")
  documents = []
  for f in files:
    content = ""
    file = open(directory + '/' + f, 'r+')
    content = file.read()
    if(content == ""):
      continue
    content = convert_text(content)

    if (word == True):
      document = document2json.document_json(title=f, content=content, words= ViTokenizer.tokenize(content), lang="vietnamese")
    else:
      document = document2json.document_json(title=f, content=content, lang="english")
    documents.append(document)
    file.close()
  mongo.bulk_insert("documents", documents)


if __name__ == '__main__':
  directoryCnet = '/home/tmc/Documents/NLP/cross_language/tech/cnet_en'
  directoryEng = '/home/tmc/Documents/NLP/cross_language/tech/en'
  directoryVi = '/home/tmc/Documents/NLP/cross_language/tech/vi'
  insertCorpus(directoryVi, word= True)
  insertCorpus(directoryEng)
  insertCorpus(directoryCnet)