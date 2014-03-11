from os import listdir
from os.path import isfile, join

from Utilities.Text import Text
from Utilities.FunctionalNGram import FunctionalNGram as FNG
from Utilities.FunctionalNGram import combine_n_gram_features as combine

from sklearn import svm
from pprint import pprint
import numpy as np

def main():
	path = "./Texts/"
	files = [f for f in listdir(path) if isfile(join(path, f))]

	n_gram_probability_features, n_grams = combine([FNG(Text(path + f)) for f in files])

	# print files
	# print n_gram_probability_features

	x = {
		"train" : n_gram_probability_features[[0, 2, 4, 5, 6, 7], :],
		"test" : n_gram_probability_features[[1, 3], :]
		}

	# It is possible to achieve good results with nu = gamma = .1 and with
	# a radial basis function kernel.
	for kernel in ["rbf", "linear", "sigmoid", "poly"]:
		for nu in np.linspace(0.0,10.0,200):
			for gamma in np.linspace(0.0,10.0,200):

				clf = svm.OneClassSVM(nu = 0.03, kernel = kernel, gamma = 0.1)
				clf.fit(x["train"])

				y = {
					"train" : clf.predict(x["train"]),
					"test" : clf.predict(x["test"])
				}
				pprint({"nu" : nu, "gamma" : gamma, "y" : y, "kernel" : kernel})

				if all(y["train"] == 1.0) and all(y["test"] == -1.0):
					raw_input()




if __name__ == "__main__":
	main()