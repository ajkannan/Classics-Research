from os import listdir
from os.path import isfile, join

from Utilities.Text import Text
from Utilities.FunctionalNGram import FunctionalNGram as FNG
from Utilities.FunctionalNGram import combine_n_gram_features as combine

from sklearn import svm
from pprint import pprint
import numpy as np

from sklearn.decomposition import PCA

def main():
	path = "./Texts/"
	files = [f for f in listdir(path) if isfile(join(path, f))]

	# Extract n gram probability features from the texts and 
	# construct them as a numpy 2D array. We also returns the 
	# n grams under consideration in the experiments here, 
	# although we have no particular use for them.
	n_gram_probability_features, n_grams = combine([FNG(Text(path + f)) for f in files])

	apply_pca = True

	if apply_pca:
		pca = PCA(n_components = 2000)
		x = {
			"train" : pca.fit_transform(n_gram_probability_features[[0, 2, 4, 5, 6, 7], :]),
			"test" : pca.transform(n_gram_probability_features[[1, 3], :])
			}
	else:
		x = {
			"train" : n_gram_probability_features[[0, 2, 4, 5, 6, 7], :],
			"test" : n_gram_probability_features[[1, 3], :]
			}

	
	# Unfortunately, it does not appear to be possible to derive a perfect
	# accuracy solution in the grid search specified below. However, it is
	# provided here anyway for educational purposes.
	grid_search = True

	if grid_search:
		for kernel in ["rbf", "linear", "sigmoid", "poly"]:
			for nu in np.linspace(0.001,1.0,200):
				for gamma in np.linspace(0.0,10.0,200):

					clf = svm.OneClassSVM(nu = nu, kernel = kernel, gamma = gamma)
					clf.fit(x["train"])

					y = {
						"train" : clf.predict(x["train"]),
						"test" : clf.predict(x["test"])
						}
				

					if all(y["train"] == 1.0) and all(y["test"] == -1.0):
						pprint({"nu" : nu, "gamma" : gamma, "y" : y, "kernel" : kernel})
						raw_input()


	# It is possible to achieve good results with nu = gamma = .1 and with
	# a radial basis function kernel.
	nu, kernel, gamma = 0.1, "rbf", 0.1
	clf = svm.OneClassSVM(nu = nu, kernel = kernel, gamma = gamma)
	clf.fit(x["train"])

	y = {
		"train" : clf.predict(x["train"]),
		"test" : clf.predict(x["test"])
	}
	pprint({"nu" : nu, "gamma" : gamma, "y" : y, "kernel" : kernel})





if __name__ == "__main__":
	main()