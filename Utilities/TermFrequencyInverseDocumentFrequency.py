from Text import Text
from pprint import pprint

import numpy as np

class TermFrequencyInverseDocumentFrequency(object):
	"""docstring for TermFrequencyInverseDocumentFrequency"""
	def __init__(self, text):
		super(TermFrequencyInverseDocumentFrequency, self).__init__()
		
		if type(text) is not Text:
			raise Exception("Invalid input to FunctionalNGram class. Only provide inputs of type Text.")

		self.corpus = []
		self.corpus_frequencies = {}

		self.add_text_to_corpus(text)


	def add_text_to_corpus(self, text):
		text_word_list = text.list
		text_frequencies = self.calculate_normalized_frequencies(text_word_list)
		
		self.corpus.append((text.name, text_frequencies))



	def calculate_normalized_frequencies(self, text_word_list, add_text = True):
		text_frequencies = {}
		length = float(len(text_word_list))

		for word in text_word_list:
			text_frequencies[word] = text_frequencies.get(word, 0.0) + 1.0
	
			if add_text:
				self.corpus_frequencies[word] = self.corpus_frequencies.get(word, 0.0) + 1.0

		for word in text_frequencies.keys():
			text_frequencies[word] /= length

		return text_frequencies

	def calculate_similarity_scores(self, text):
		query_text_frequencies = self.calculate_normalized_frequencies(text.list, add_text = False)

		similarities = []

		for document in self.corpus:
			similarity_score = 0.0

			document_frequencies = document[1]

			for word in query_text_frequencies.keys():

				if word in document_frequencies.keys():
					similarity_score += (query_text_frequencies[word] / self.corpus_frequencies[word]) + (
						document_frequencies[word] / self.corpus_frequencies[word]
						)

			similarities.append((document[0], similarity_score))

			return similarities

	def calculate_features_for_corpus(self):		
		features = np.zeros((len(self.corpus), len(self.corpus_frequencies.keys())))
		
		for i, document in enumerate(self.corpus):
			for j, word in enumerate(self.corpus_frequencies.keys()):

				if word in document[1].keys():
					features[i, j] = document[1][word]
				else:
					features[i, j] = 0.0

		return features, self.corpus_frequencies.keys()



text = Text("../Texts/agamemnon.txt")
tfidf = TermFrequencyInverseDocumentFrequency(text)
tfidf.add_text_to_corpus(Text("../Texts/oedipus.txt"))
tfidf.add_text_to_corpus(Text("../Texts/medea.txt"))

pprint(tfidf.calculate_similarity_scores(text))
pprint(tfidf.corpus[0])

features, word_list = tfidf.calculate_features_for_corpus()

np.savetxt('test.txt', features)
