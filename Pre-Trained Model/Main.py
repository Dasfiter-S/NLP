import sys
import copy
import numpy as np
import nltk
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec
from nltk.corpus import brown

'''
First retreiving synsets. Every Synset contains
an example sentence which shows how the word is used in context. Finds 
similarity between examples and input sentence to retreive synsets with similar
context, after which it finds synonyms of every synset matched with word.
'''

b = Word2Vec(brown.sents())  # Initialzing word2vec with brown dataset


def calculate_sent_similarity(sent1, sent2):
    '''
    Calculates cosine similarity between two sentences, by first
    retrieving word2vec for every word in sentence, then taking a
    mean to generate a mean vector for each sentence.

    '''


    sent1_vec = []
    sent2_vec = []
    for word in sent1:
        try:
            sent1_vec.append(b.wv[word])
        except Exception as e:  # Check for KeyError
            continue
    for word in sent2:
        try:
            sent2_vec.append(b.wv[word])  # Check for KeyError
        except Exception as e:
            continue

    vA = np.mean(sent1_vec, axis=0)
    vB = np.mean(sent2_vec, axis=0)

    return (np.dot(vA, vB) / (np.linalg.norm(vA) * np.linalg.norm(vB)))


def get_synsets(sent, word):
    '''
    Each synset contains one or more lemmas, which represent a specific sense of a specific word.
    accepted_synsets: Dictionary of synsets that have the same parts of speech as the word in the sentence, with similarity score as their value.
    rejected_synsets: Dictionary of remaining synsets.
    synsets_all: Combined Dictionary
    '''


    sent = sent.split()
    tag = nltk.pos_tag(sent)  # Tagging, finding parts of speech in sentence
    pos = ''
    for w in tag:
        if w[0] == word:
            pos = w[1][0].lower()
        if pos == 'j':  # wordnet uses 's' for adjective while tagger uses 'j'
            pos = 's'
        break
    accepted_synsets = []
    rejected_synsets = []
    for syn in wn.synsets(word):
        st = str(syn)
        st = st[st.find('.') + 1:-1]
        st = st[:st.find('.')]
    if st == pos:
        accepted_synsets.append(syn)
    else:
        rejected_synsets.append(syn)

    # Creating dictionaries with scores
    accepted_synsets_scores = {}
    for syn in accepted_synsets:
        if len(syn.examples()) > 0:
            # Finding similarity scores between example synset sentence and input sentence
            # Utilzing sentence context here
            score = calculate_sent_similarity(sent, syn.examples()[0].split())
            accepted_synsets_scores[syn] = score

    rejected_synsets_scores = {}
    for syn in rejected_synsets:
        if len(syn.examples()) > 0:
            # Finding similarity scores between example synset sentence and input sentence
            # Utilzing sentence context here
            score = calculate_sent_similarity(sent, syn.examples()[0].split())
            rejected_synsets_scores[syn] = score

    synsets = wn.synsets(word)

    synsets_all = {}
    for syn in synsets:
        if len(syn.examples()) > 0:
            # Finding similarity scores between example synset sentence and input sentence
            # Utilzing sentence context here
            score = calculate_sent_similarity(sent, syn.examples()[0].split())
            synsets_all[syn] = score

    return accepted_synsets_scores, rejected_synsets_scores, synsets_all


def get_synonyms(sent, word):
    '''
    Selects synonyms by first using only accepted_synsets, otherwise
    utilizes rejected_synsets
    Returns: List of synonyms
    '''


    accepted_synsets, rejected_synsets, synsets = get_synsets(sent, word)

    accepted_scores = sorted(accepted_synsets.values(), reverse=True)
    rejected_scores = sorted(rejected_synsets.values())

    scores = copy.deepcopy(accepted_scores) + copy.deepcopy(rejected_scores)
    scores = scores[:4]
    synonyms = []
    for score in scores:
        for syn in synsets.keys():
            if synsets[syn] == score:
                for l in syn.lemmas():  # Loop to get synonyms

                    if l.name() != word and l.name() not in synonyms:
                        synonyms.append(l.name())

    return synonyms


def get_synonyms_sentence(sent, word):
    '''
    Returns sentences with synonyms in place of the actual word
    '''


    syns = get_synonyms(sent, word)
    syn_sents = []
    temp = sent.split()
    i = temp.index(word)
    for s in syns:
        temp[i] = s
        syn_sents.append(temp.copy())

    return syn_sents  # Returns a list of sentences with synonyms

if __name__ == '__main__':

    sent = input('Enter Sentence: ')
    word = input('Enter Word: ')
    sent = sent.replace('?', '').replace('.', '')  # Preprocessing
    if word in sent.split():
        syn_sents = get_synonyms_sentence(sent, word)
        print('\nGenerated Sentences: ')
        for s in syn_sents:
            print(' '.join(s))
    else:
        print('Word not in Sentence.')
