from Text import Text

from pprint import pprint
import numpy as np
import string
import itertools
import copy

def combine_n_gram_features(n_gram_probabilities):
	""" Compiles n-gram probability features into numpy array

	Parameters
	----------
	n_gram_probabilities:

	Returns
	-------
	features and respective n-grams
	"""
	if type(n_gram_probabilities) is not list:
		raise Exception("Invalid input to method. Only provide a list object.")


	features = np.zeros((len(n_gram_probabilities), len(n_gram_probabilities[0].probability_features.keys())))

	# I think this works as a sanity check.
	# for i, text_features in enumerate(n_gram_probabilities):
	#  	for j, n_gram in enumerate(n_gram_probabilities[0].probability_features.keys()):
	#  		features[i, j] = text_features.probability_features[n_gram]
	# pprint(features)

	# This is probably more efficient however.
	for i, text_features in enumerate(n_gram_probabilities):
		features[i, :] = np.array(text_features.probability_features.values())

	return features, n_gram_probabilities[0].probability_features.keys()




class FunctionalNGram(object):
	""" Represents the functional n-gram feature representation of the text"""
	def __init__(self, text, n = 2):
		""" Calls functions to calculate probabilities of n-grams

		Parameters
		----------
		n: size of lettergram

		Returns
		-------
		None
		"""

		super(FunctionalNGram, self).__init__()

		if type(text) is not Text:
			raise Exception("Invalid input to FunctionalNGram class. Only provide inputs of type Text.")

		self.text = text
		self.find_n_grams(n)
		self.compute_probability_features()


	def find_n_grams(self, n):
		""" Iterates through text finding frequencies of n-grams

		Parameters
		----------
		n: size of lettergram

		Returns
		-------
		None
		"""

		n_grams = self.initialize_n_grams(n)
		text = self.text.processed_text

		for line in text:
			joined_line = " ".join(line)
			for i in xrange(len(joined_line) - n + 1):
				n_gram = tuple([joined_line[i + j] for j in xrange(n)])
				if n_gram in n_grams.keys():
					n_grams[n_gram] += 1.0

		self.n_grams = n_grams


	def initialize_n_grams(self, n):
		""" Initializes n-gram dictionary.

		Keys of the dictionary are all possible n-grams of alphabetical letters
		and spaces (punctuation not included). Values in the dictionary are the
		respective frequencies.

		Parameters
		----------
		n: size of lettergram

		Returns
		-------
		dictionary mentioned above
		"""

		n_grams = {}
		keys = []
		letters = ' ' + string.ascii_lowercase
		for letter_1 in letters:
			keys.append([letter_1])

		for i in xrange(1, n):
			# Add next character to each key
			keys_old_copy = copy.copy(keys)
			for key in keys_old_copy:
				for letter in letters:
					new_key = copy.copy(key)
					new_key.append(letter)
					keys.append(new_key)

			# Remove shorter keys
			keys_old_copy = copy.copy(keys)
			for key in keys_old_copy:
				if len(key) < i + 1:
					keys.remove(key)

		for key in keys:
			n_grams[tuple(key)] = 0.0

		return n_grams


	def compute_probability_features(self):
		""" Computes probability features

		Parameters
		----------
		None

		Returns
		-------
		None
		"""

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


if __name__ == "__main__":
	n_gram = FunctionalNGram()
