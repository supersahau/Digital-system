#coding=utf-8
import os
import numpy as np
import jieba.posseg
import scipy
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import lda
import sys
import lda.datasets
from Hcluster import hcluster
import pickle
import readcsv

# 存储读取语料 一行预料为一个文档
def realVirWords():
    with open("corpusVirCut.txt", 'rb') as savefile:    
        corpusvir = pickle.load(savefile)
    return corpusvir

# generate the model of LDA
def genLDAmodel(corpus):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    analyze = vectorizer.build_analyzer()
    weight = X.toarray()
    vc = list(vectorizer.get_feature_names())
    for i in range(len(vc)):
        if vc[i][0:2] == "填充":
            vc[i] = vc[i][2:]

    
    #print(len(vectorizer.vocabulary_))
    #print(len(lda.datasets.load_reuters_vocab()))
    originvc = list(vectorizer.get_feature_names())
    model = lda.LDA(n_topics=50, n_iter=500, random_state=1)
    model.fit(np.asarray(weight.astype(np.int32)))  # model.fit_transform(X) is also available
    return model,vc,originvc

# demonstrate the model(topicword and doctopic)
def demonstarateModel(model,vc):
    topic_word = model.topic_word_  # model.components_ also works
    # 文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))
    vocab = tuple(vc)
    # 输出主题的分布(vis the first n_top_word words)
    label2 = []
    n_top_words = 7
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

def testModel(model,titles,newdocnumber,originvc):
    # load the test corpus
    n_weight = np.zeros((newdocnumber, len(originvc))) # 30 docs now
    n_corpus = [] # the test corpus
    for i in range(40, 50):
        for j in range(len(titles)):
            f = open("corpvir/" + titles[j] + str(i) + "g.txt", 'r', encoding='utf-8')
            tmp = f.read()
            n_corpus.append(tmp.split())

    lent = 0
    # calculate the rate of existing words
    for i in range(len(n_corpus)):
        lent = 0
        for word in n_corpus[i]:
            for j in range(len(originvc)):
                if word == originvc[j]:
                    n_weight[i][j] += 1
                    lent += 1
                    break
        print((i+120), '  ', lent / len(n_corpus[i])) # print rate

    B = np.asarray(n_weight.astype(np.int32))
    C = model.transform(B, max_iter=500, tol=1e-16)
    outcome = np.concatenate((model.doc_topic_, C))
    return outcome

def Doc_cluster(outcome):
    # 输出文章的主题分布
    label = []
    for n in range(len(outcome)):
        label.append(outcome[n])

    k, l = hcluster(outcome, 25)
    print(l)
    for subl in l:
        subl.sort()
    for i in range(len(l)):
        if len(l[i]) >= 1:
            for j in range(len(l[i])):
                print("doc: {}".format( l[i][j] ))
                #print("type: {} doc: {} topic: {}".format( (l[i][j] % 3),l[i][j], label[l[i][j]]))
        print('\n')

if __name__ == "__main__":
    tag = 1
    if tag:
        corpus = realVirWords()
        model,vc,originvc = genLDAmodel(corpus)
        with open("ldamodel.txt", 'wb') as savefile:    
            pickle.dump(model,savefile)
        with open("ldavc.txt", 'wb') as savefile:    
            pickle.dump(vc,savefile)
        with open("ldaoriginvc.txt", 'wb') as savefile:    
            pickle.dump(originvc,savefile)
    else:
        with open("ldamodel.txt", 'rb') as savefile:    
            model = pickle.load(savefile)
        with open("ldavc.txt", 'rb') as savefile:    
            vc = pickle.load(savefile)
        with open("ldaoriginvc.txt", 'rb') as savefile:    
            originvc = pickle.load(savefile)
    #demonstarateModel(model,vc)
    #titles = ["bd","mm","zjw"]
    #newdocnumber = 30
    #outcome = testModel(model,titles,newdocnumber,originvc)
    #print(len(outcome))
    outcome = model.doc_topic_
    with open("virVec.txt", 'wb') as savefile:    
            pickle.dump(outcome,savefile)
    #Doc_cluster(outcome)
   



