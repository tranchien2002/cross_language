# -*- coding: utf-8 -*-
import database as mydb
from os import listdir
import pdb
from sklearn.feature_extraction.text import TfidfVectorizer
from underthesea import word_tokenize
from pyvi import ViTokenizer
from Article import Article

def convert_text(text):
  converted = text.replace('“', '')
  converted = converted.replace('”', '')
  converted = converted.replace("’", "")
  converted = converted.replace("'", "")
  converted = converted.replace('"', '')
  return converted.lower()

def list_files(directory, extension):
  return (f for f in listdir(directory) if f.endswith('.' + extension))

def insertCorpus(directory, table_store, word = "false"):
  files = list_files(directory, "txt")
  for f in files:
    content = ""
    file = open(directory + '/' + f, 'r+')
    content = file.read()
    content = convert_text(content)
    print(content)
    if (word == "true"):
      mydb.insert("INSERT INTO " + str(table_store) + " (title, content, word) VALUES (%s, %s, %s) ",
                  (f, content, ViTokenizer.tokenize(content)))
    else:
      mydb.insert("INSERT INTO " + str(table_store) + " (title, content) VALUES (%s, %s) ",
                  (f, content))
    file.close()


def insertIDF(table_store):
  articles = mydb.execute_query("SELECT id, content, word FROM " + table_store)
  list_articles = [Article(item[0], item[1], item[2]) for item in articles]
  contents = [item.content for item in list_articles]
  tf = TfidfVectorizer(use_idf=True)
  tf.fit_transform(contents)
  idf = tf.idf_
  pdb.set_trace()
  mydb.insert("INSERT INTO idf (" + str(table_store) + ") VALUES (%s)", (idf))

if __name__ == '__main__':
  directoryVi = '/home/tmc/Documents/NLP/cross_language/tech/vi'
  # directoryEng = '/home/tmc/Documents/NLP/cross_language/tech/en'
  directoryEng = '/home/tmc/Documents/NLP/cross_language/tech/cnet_en'

  insertCorpus(directoryEng, "english")
  insertCorpus(directoryVi, "vietnamese", word="true")

