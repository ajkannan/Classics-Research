from os import listdir
from os.path import isfile, join

from Utilities.Text import Text
from Utilities.FunctionalNGram import FunctionalNGram as FNG
from Utilities.FunctionalNGram import combine_n_gram_features as combine

def main():
	path = "./Texts/"
	files = [f for f in listdir(path) if isfile(join(path, f))]

	n_gram_probability_features, n_grams = combine([FNG(Text(path + f)) for f in files])

	print files
	print n_gram_probability_features



if __name__ == "__main__":
	main()