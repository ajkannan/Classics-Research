Classics-Research
=================

This is code written by James Brofos and Ajay Kannan for performing similarity analysis on Latin tragedies written by the Roman statesman Seneca the Younger. Essentially, the central idea of this work is to provide quantitative analysis for an authorship attribution problem revolving around Seneca. Two of Seneca's plays "Octavia" and "Hercules Oetaeus" are disputed as having been written by Seneca. 

## Features

Besides standard inference algorithms that leverage the results of machine learning, we also implement several key text-representation methods. In particular, we implement:

- Term-frequency inverse document frequency
- Functional n-gram probabilities

## Demo

The following code constructs functional n-gram representations of the eight tragedies by Seneca. There exist methods for performing a grid-search of the one-class SVM parameter space to find possibilities for a perfect classifier. No such parameter settings are found in the space (which may be a good thing so as to avoid over-fitting), yet there is a known setting of the parameters to train an effective model. The results of this model are displayed to the user. In particular, the one-class SVM predicts that "Octavia" and "Hercules Oetaeus" were not written by Seneca. 

```
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
	pprint(files)

	# Extract n gram probability features from the texts and 
	# construct them as a numpy 2D array. We also returns the 
	# n grams under consideration in the experiments here, 
	# although we have no particular use for them.
	features, n_grams = combine([FNG(Text(path + f)) for f in files])

	apply_pca = False

	if apply_pca:
		pca = PCA(n_components = features.shape[1])
		x = {
			"train" : pca.fit_transform(features[[0, 2, 4, 5, 6, 7], :]),
			"test" : pca.transform(features[[1, 3], :])
			}
	else:
		x = {
			"train" : features[[0, 2, 4, 5, 6, 7], :],
			"test" : features[[1, 3], :]
			}

	
	# Unfortunately, it does not appear to be possible to derive a perfect
	# accuracy solution in the grid search specified below. However, it is
	# provided here anyway for educational purposes.
	grid_search = False

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


	# It is possible to achieve good results with nu = gamma = .1 and with
	# a radial basis function kernel.
	nu, kernel, gamma = 0.1, "rbf", 0.1
	clf = svm.OneClassSVM(nu = nu, kernel = kernel, gamma = gamma)
	clf.fit(x["train"])

	y = {
		"train" : clf.predict(x["train"]),
		"test" : clf.predict(x["test"])
	}

	metrics = {
		"train" : clf.decision_function(x["train"]),
		"test" : clf.decision_function(x["test"])
	}

	pprint({"nu" : nu, "gamma" : gamma, "y" : y, "kernel" : kernel, "metrics" : metrics})


if __name__ == "__main__":
	main()
```

## Dependencies

* [Numpy](http://www.numpy.org/) Standard numerical computations with vectors
* [Scipy](http://www.scipy.org/) Used for calculations involving statistical distributions
* [scikit-learn](http://scikit-learn.org/stable/) Python machine learning library


