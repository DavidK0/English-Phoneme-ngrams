import argparse
import csv
import re

from nltk.lm import MLE
from itertools import chain
from nltk.util import everygrams

parser = argparse.ArgumentParser(description="Read a CSV file")
parser.add_argument('file', type=str, help="Path to the CSV file")
parser.add_argument('-n', type=int, help="Size of the n-gram model", default=3)
args = parser.parse_args()

CMUPD_to_IPA = {"AA": "ɑ",
                "AE": "æ",
                "AH": "ʌ",
                "AO": "ɔ",
                "AW": "aʊ",
                "AY": "aɪ",
                "B": "b",
                "CH": "tʃ",
                "D": "d",
                "DH": "ð",
                "EH": "ɛ",
                "ER": "ɚ",
                "EY": "eɪ",
                "F": "f",
                "G": "ɡ",
                "HH": "h",
                "IH": "ɪ",
                "IY": "i",
                "JH": "dʒ",
                "K": "k",
                "L": "l",
                "M": "m",
                "N": "n",
                "NG": "ŋ",
                "OW": "oʊ",
                "OY": "ɔɪ",
                "P": "p",
                "R": "r",
                "S": "s",
                "SH": "ʃ",
                "T": "t",
                "TH": "θ",
                "UH": "ʊ",
                "UW": "u",
                "V": "v",
                "W": "w",
                "Y": "j",
                "Z": "z",
                "ZH": "ʒ"}

# Split a string like "AH0" into its two parts, the phoneme ("AH") and stress ("0")
# Returns just the phoneme part
def phoneme_stress_string_split(string):
    pattern = r"([A-Za-z]+)(\d+)?"
    match = re.match(pattern, string)
    letters_part = match.group(1) # Phoneme
    #numbers_part = match.group(2) if match.group(2) else None # Stress
    return letters_part

# This class hold some information about a word
class WordInfo:
    def __init__(self, word, frequency, pronunciation):
        self.word = word
        self.frequency = frequency
        self.pronunciation = pronunciation

    def __str__(self):
        return f"{self.word} ({self.frequency}) {''.join(self.pronunciation)}"

# Load the PFD
PFD = []
with open(args.file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        word = row[0]
        frequency = row[1]

        # Process the pronunciation
        pronunciation = row[2:]
        pronunciation = [phoneme_stress_string_split(phoneme) for phoneme in pronunciation]
        pronunciation = [CMUPD_to_IPA[phoneme] for phoneme in pronunciation]

        new_word = WordInfo(word, int(frequency), pronunciation)
        PFD.append(new_word)

# prepare data for n-gram model
#   pad the words with seperator tokens
train_data = []
for word in PFD:
    frequency_factor = .01
    modified_frequency = int(word.frequency * frequency_factor)
    
    padded_pronunciation = ["<sep>"] + word.pronunciation + ["<sep>"]
    train_data.extend([padded_pronunciation ] * modified_frequency)

train = (everygrams(list(word), max_len=args.n) for word in train_data)
vocab = chain.from_iterable(train_data)

# create and train model
lm=MLE(args.n)
lm.fit(train, vocab)

# generate new word data
new_word_data = lm.generate(100)

# process the word data into words
curr_word = []
new_words = []
for phoneme in new_word_data:
    if phoneme == "<sep>":
        if curr_word != []:
            new_words.append(curr_word)
        curr_word = []
    else:
        curr_word.append(phoneme)

# Print new words
words_to_generate = 10
words_generated = 0
for new_word in new_words:
    is_english = False
    for word in PFD:
        if new_word == word.pronunciation:
            is_english = True
            #print("".join(new_word))
    if not is_english:
        pass
        print("".join(new_word))