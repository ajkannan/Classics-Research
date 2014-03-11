
from pprint import pprint
import re

from os.path import split

class Text(object):
	"""docstring for Text"""
	def __init__(self, file_path):
		super(Text, self).__init__()

		self.open_file_path(file_path)
		self.preprocess_raw_text()
		self.concatenate_processed_text()
		self.generate_list_of_words()

		self.name = split(file_path)[-1]

	def open_file_path(self, file_path):
		text = []
		with open(file_path, "r") as f:
			for line in f:
				text.append(line)

		self.raw = text

	def preprocess_raw_text(self, lower_case = True, punctuation = "delete"):
		processed_text = []
		for line in self.raw:
			processed_line = self.process_line(line, lower_case, punctuation)
			if len(processed_line):
				processed_text.append(processed_line)

		self.processed_text = processed_text

	def process_line(self, line, lower_case, punctuation):
		# Removes line numbers and other numeric strings from this line of
		# the play.
		processed_line = [word for word in line.split() if not word.isdigit()]


		# Removes the speaker indicator from this particular line. Speakers are
		# indicated by the convention "[SPEAKER]". If the option is specified as
		# True, then these remaining words are also converted to their lower 
		# case form in this step.
		processed_line = [word.lower() if lower_case else word for word in processed_line if word[0] != "[" and word[-1] != "]"]

	
		if punctuation == "separate":
			# In the event that we wish to separate punctuation from neighboring 
			# words, then we employ the regular expression tool to create the 
			# separated list.
			processed_line = re.findall(u"[\w']+|[.,!?;]", " ".join(processed_line))

		elif punctuation == "delete":
			# In the event that we wish to delete punctation from the text, 
			# we employ the regular expressions tool to separate punctuation and 
			# subsequently remove punctuation from the resulting list.
			punctuation_set = set([".", ",", "!", "?", ";"])

			separated_punctuation = re.findall(u"[\w']+|[.,!?;]", " ".join(processed_line))
			punctuation_removed = ["".join(c for c in s if c not in punctuation_set) for s in separated_punctuation]
			processed_line = [word for word in punctuation_removed if word != ""]

		return processed_line

	def concatenate_processed_text(self):
		concatenated_text = ""
		for line in self.processed_text:
			concatenated_text += " ".join(line) + " "


		# Remove the trailing space character from the concatenated string
		# of words.
		concatenated_text = concatenated_text[:-1]

		self.concatenated_text = concatenated_text

	def generate_list_of_words(self):
		self.list = self.concatenated_text.split()


# text = Text("../Texts/agamemnon.txt")

# text.preprocess_raw_text()
# text.concatenate_processed_text()

# pprint(text.processed_text)
# pprint(text.concatenated_text)



