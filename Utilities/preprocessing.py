from pprint import pprint
import re

def process_line(line, lower_case = True, punctuation = "delete"):

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


def open_file(file_path):
	text = []

	with open(file_path, "r") as f:
		for line in f:
			processed_line = process_line(line)
			if len(processed_line) > 0:
				text.append(processed_line)

	return text


def main():
	file_path = "../Texts/agamemnon.txt"
	text = open_file(file_path)
	pprint(text)



if __name__ == "__main__":
	main()

