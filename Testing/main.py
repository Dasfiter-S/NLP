from train_utils import train, unused_dictionary, reverse_dictionary
import numpy as np
import sys
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

# Number of synonyms to find
num_of_syns = 10

def get_embedding(word, weights):
    index = unused_dictionary[word]
    return weights[index]

def calculate_cosine_similarity(vA,vB):
    return (np.dot(vA, vB) / (np.linalg.norm(vA) * np.linalg.norm(vB)))

def most_similar(word, weights):
	try:
	    weights_word = get_embedding(word,weights)
	except KeyError:
		print('Word Not Found in Vocabulary!')
		sys.exit(0)

	top_n_s = [-1] * num_of_syns
	top_n = list(range(num_of_syns))
	for idx,weight in enumerate(weights):
	    sim = calculate_cosine_similarity(weights_word, weight)
	    for i,n in enumerate(top_n_s):
		    if n < sim:
		        top_n_s[i] = sim
		        top_n[i] = idx
		        break
	similar = []
	for t in top_n:
		similar.append(reverse_dictionary[t])
	return similar

def get_synonyms(word, weights):
	similar = most_similar(word, weights)
	synonyms = []
	antonyms = []
	for syn in wordnet.synsets(word): # Remove all antonyms
	    for l in syn.lemmas(): 
	        if l.antonyms(): 
	            antonyms.append(l.antonyms()[0].name())

	for s in similar:
		if s != word and s not in antonyms:
			synonyms.append(s)

	return synonyms


def get_synonyms_sentence(sent, word, weights):
    sent = sent.split()
    syns = get_synonyms(word, weights)
    syn_sents = []
    temp = sent
    i = sent.index(word)
    for s in syns:
        temp[i] = s
        syn_sents.append(temp.copy())
        
    return syn_sents #Returns a list of sentences with synonyms

if __name__ == '__main__':
	num_steps = 1000001
	print('Loading Weights...')
	if len(sys.argv) > 1:
		if sys.argv[1] == 'train':
			weights = train(num_steps)
		else:
			print('Invalid Argument, Exiting...')
			sys.exit(0)
	else:
		weights = np.load('weights.npy')

	print('Weights Loaded!')
	sent = input('Enter Sentence: ')
	word = input('Enter Word: ')
	if word in sent.split():
		syn_sents = get_synonyms_sentence(sent, word, weights)
		print('\nGenerated Sentences: ')
		for s in syn_sents:
			print(' '.join(s))
	else:
		print('Word not in Sentence.')