import pdb
import spacy
import Mongodb as mongo
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from document2json import pickle_json, cosine_json
import _pickle as cPickle
from bson.objectid import ObjectId
nlp = spacy.load('en_core_web_md')
docs_col = mongo.get_colection("documents")

def keyword2matrix(keywords):
    keywords = keywords.replace(",", " ")
    doc = nlp(keywords)
    vectors = [item.vector for item in doc]
    matrix = np.asmatrix(vectors)
    return matrix

def similarity(matrix1, matrix2):
    matrix1 = np.asmatrix(matrix1)
    matrix2 = np.asmatrix(matrix2)
    return cosine_similarity(matrix1, matrix2)

def square_sum(matrix):
    square_matrix = np.square(np.asmatrix(matrix))
    return square_matrix.sum()

def square_mean(matrix):
    square_matrix = np.square(np.asmatrix(matrix))
    return square_matrix.mean()

def mean_max_each_row(matrix):
    max_rows = []
    for i in range(matrix.shape[0]):
        max_rows.append(np.max(matrix[i,]))
    return np.mean(max_rows)

def store_matrix():
    documents_en = docs_col.find({"lang": 'english'})
    # pdb.set_trace()
    documents_en = [pickle_json(str(item["_id"]), keyword2matrix(item["keyword"])) for item in documents_en]
    ouf = open('pickle_en.txt', 'wb')
    cPickle.dump(documents_en, ouf)
    ouf.close()

def get_matrix_vectors():
    inf = open('pickle_en.txt', 'rb')
    matrix_vectors = cPickle.load(inf)
    return matrix_vectors

def get_list_similarity(matrix, matrices):
    new_matrices = []
    for item in matrices:
        print(item)
        if(item['matrix'] == ''):
            continue
        new_matrices.append(cosine_json(item['id'], mean_max_each_row(similarity(matrix, item['matrix']))))
    # new_matrices = [cosine_json(item['id'], square_mean(similarity(mix, item['matrix']))) for item in matrices]
    return new_matrices


def get_documents(list_docs):
    sorted_list = sorted(list_docs, key= lambda x: float(x['similarity']), reverse=True)
    return sorted_list

def get_topn_similarity_documents(keywords, n=5):
    matrix_vectors = get_matrix_vectors()
    docs = get_list_similarity(keyword2matrix(keywords), matrix_vectors)
    sorted_docs = get_documents(docs)
    return sorted_docs[:n]
#
# def get_json_docs(list_ids):
#     list_docs = []
#     for item in list_ids:
#         list_docs.append(docs_col.find_one({"_id": ObjectId(str(item['id']))}))
#     return list_docs

def get_json_docs(list_ids):
    list_docs = []
    for item in list_ids:
        doc = docs_col.find_one({"_id": ObjectId(str(item['id']))})
        doc['similarity'] = item['similarity']
        doc.pop('_id', None)
        print(doc)
        list_docs.append(doc)
    return list_docs


if __name__ == '__main__':
    store_matrix()
    # articles_vi = docs_col.find({"lang": 'vietnamese'})
    # start_time = time.time()
    # for item in articles_vi:
    #     list_ids = get_topn_similarity_documents(item['keyword'])
    #     list_docs = get_json_docs(list_ids)
    #     list_titles = [item['title'] for item in list_docs]
    #     filename = "result_matrix.txt"
    #     myfile = open(filename, 'a+')
    #     myfile.write(item['title'] + "\n")
    #     for t in list_titles:
    #         myfile.write(t + "\n")
    #     myfile.write("============================" + "\n")
    #     print(list_titles)
    # elapsed_time = time.time() - start_time
    # print(elapsed_time)






    # docs = get_list_similarity(keyword2matrix(articles_vi[6]['keyword']), matrix_vectors)
    # sorted_docs = get_documents(docs)

    # test
    # title = articles_vi[6]['title']
    # pdb.set_trace()
