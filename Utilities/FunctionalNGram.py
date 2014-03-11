from Text import Text

from pprint import pprint
import numpy as np
import string
import itertools

class FunctionalNGram(object):
	"""docstring for FunctionalNGram"""
	def __init__(self, text):
		super(FunctionalNGram, self).__init__()
		
		if type(text) is not Text:
			raise Exception("Invalid input to FunctionalNGram class. Only provide inputs of type Text.")

		self.text = text
		self.find_n_grams()

		self.compute_probability_features()

	def find_n_grams(self):
		n_grams = self.initialize_n_grams()
		text = self.text.processed_text
		n = 2

		for line in text:
			joined_line = " ".join(line)

			for i in xrange(len(joined_line) - 1):
				n_gram = tuple([joined_line[i + j] for j in xrange(n)])
				
				if n_gram in n_grams.keys():

					n_grams[n_gram] += 1.0

		self.n_grams = n_grams


	def initialize_n_grams(self):
		n_grams = {}
		letters = ' ' + string.ascii_lowercase

		for letter_1 in letters:
			for letter_2 in letters:
				n_grams[(letter_1, letter_2)] = 0.0

		return n_grams

	def compute_probability_features(self):
		n_gram_tuples = self.n_grams.keys()

		n_gram_probabilities = {}
		alphabet = {}
	
		for n_gram in n_gram_tuples:
			
			if n_gram[0] not in alphabet:
				frequency_count = 0.0

				for letter_gram in n_gram_tuples:
					if n_gram[0] == letter_gram[0]:
						frequency_count += self.n_grams[letter_gram]

				alphabet[n_gram[0]] = frequency_count

			if alphabet[n_gram[0]] > 0:
				n_gram_probabilities[n_gram] = self.n_grams[n_gram] / alphabet[n_gram[0]]
			else:
				n_gram_probabilities[n_gram] = 0.0

		self.probability_features = n_gram_probabilities


text = Text("../Texts/agamemnon.txt")
fng = FunctionalNGram(text)