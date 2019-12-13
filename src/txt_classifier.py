#!/usr/bin/env python
# coding: utf-8

# In[48]:


import math
import requests
import sqlite3
from bs4 import BeautifulSoup
import json
import nltk
import random
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode


# In[62]:


def find_features_job(ind,word_features):
    words = set(ind)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# In[63]:


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


# In[64]:


def train(trainfile):
    with open(trainfile,'r') as f:
        data = f.read().split('\n')
        f.close()

    document_job = []
    for item in data:
        filtered = []
        word_tokens = word_tokenize(item)
        label = word_tokens[0] + word_tokens[1]
        filtered = word_tokens[2:]
        add_material = (filtered, label)
        document_job.append(add_material)

    all_words = []
    for item in document_job:
        for word in item[0]:
            all_words.append(word.lower())

    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:1800]
    
    def find_features_job(ind):
        words = set(ind)
        features = {}
        for w in word_features:
            features[w] = (w in words)

        return features

    featuresets = [(find_features_job(rev), category) for (rev, category) in document_job]
    
    training_set = featuresets[:]

    classifier_0 = nltk.NaiveBayesClassifier.train(training_set)

    classifier_1 = SklearnClassifier(MultinomialNB())
    classifier_1.train(training_set)

    classifier_2 = SklearnClassifier(BernoulliNB())
    classifier_2.train(training_set)

    classifier_3 = SklearnClassifier(LogisticRegression())
    classifier_3.train(training_set)

    classifier_4 = SklearnClassifier(SGDClassifier())
    classifier_4.train(training_set)

    classifier_5 = SklearnClassifier(LinearSVC())
    classifier_5.train(training_set)

    classifier_6 = SklearnClassifier(NuSVC())
    classifier_6.train(training_set)
    
    combined_classifier = VoteClassifier(classifier_0,
                                      classifier_1,
                                      classifier_2,
                                      classifier_3,
                                      classifier_4,
                                      classifier_5,
                                      classifier_6)

    save_classifier = open("./data/naivebayes.pickle","wb")
    pickle.dump(combined_classifier, save_classifier)
    save_classifier.close()
    return word_features


# In[65]:


if __name__ == "__main__":
    with open('../data/desc_database.json','r') as f:
        data_spec = json.load(f)

    word_features = train('../data/classifier.txt')    
    f = open("../data/naivebayes.pickle", "rb")
    combined_classifier = pickle.load(f)
    f.close()
    n = 0
    for item in data_spec.keys():
        test_document = data_spec[item]['description']
        sentence_test = test_document.split('\n')
        req = []
        des = []
        for sentence in sentence_test:
            #'' means nothing, so just skip
            if sentence ==  '':
                continue
            word_test_list = word_tokenize(sentence.lower())
            featureset = find_features_job(word_test_list,word_features)
            if combined_classifier.classify(featureset) == '@req':
                req.append(sentence)
            elif combined_classifier.classify(featureset) == '@des':
                des.append(sentence)
        data_spec[item]['req'] = req
        data_spec[item]['des'] = des
        print(f'{item} out of {len(data_spec.keys())}')
        n += 1
        if n == 100:
            break


# In[ ]:




