import json

def document_json(title, content, words = "", keyword = "", lang=""):
    return ({'title': title, 'content': content, 'words': words, 'keyword': keyword, 'lang': lang})

def pickle_json(id, matrix):
    return {'id': id, 'matrix': matrix}

def cosine_json(id, similarity):
    return {'id': id, 'similarity': similarity}

def lsh_json(id, keyword):
    return {'id': id, 'keyword': keyword}

def ngram_json(id, content):
    return {'id': id, 'content': content}