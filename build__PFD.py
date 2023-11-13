# This scripts takes one optional argument:
#  * the output file to save the pronunciation-frequency dictionary (default: PFD.csv)

# This script automatically downloads the two necessary text corpora:
#  * the CMU Pronunciation Dictionary (https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b)
#  * the Word Frequencies in Written and Spoken English (https://ucrel.lancs.ac.uk/bncfreq/lists/1_1_all_alpha.txt)

# It find the set intersection between words in the two corpora 
#  and outputs the combined pronunciation/frequency data to the output file.

import sys
import csv
import requests

# The output file to save the pronunciation-frequency dictionary (PFD)
PFD_file = sys.argv[1] if len(sys.argv) > 1 else "PDF.csv"

# URLs for the required files
CMUPD_url = "https://raw.githubusercontent.com/Alexir/CMUdict/master/cmudict-0.7b"
WFWSE_url = "https://ucrel.lancs.ac.uk/bncfreq/lists/1_1_all_alpha.txt"

# Function to download a file from a URL
def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return response.text.splitlines()

# Load the CMU Pronunciation Dictionary (CMUPD).
# For words with multiple pronunciations, only the first one is used
CMUPD_lines = download_file(CMUPD_url)
CMUPD = {}
for line in CMUPD_lines:
    # skip comment lines
    if line[:3] == ";;;":
        continue
    
    # normalize the word
    word = line.split()[0].lower()
    if word[-1] == ")":
        word = word[:-3]
    
    if word not in CMUPD:
        CMUPD[word] = line.split()[1:]

# Load the Word Frequencies in Written and Spoken English (WFWSE).
WFWSE_lines = download_file(WFWSE_url)
WFWSE = {}
for line in WFWSE_lines[1:]:  # skip header
    line = line.split("\t")[1:]
    if line[0] == "@":
        word = line[2]
    else:
        word = line[0]
    word = word.lower()
    
    # some words are malformed and must be skipped
    if word not in WFWSE and len(line) >= 4 and "#" not in line[3]:
        WFWSE[word] = line[3]

# Find set intersection between CMUPD and WFWSE
PFD = []
for word in CMUPD:
    if word in WFWSE:
        PFD.append([word, WFWSE[word]] + CMUPD[word])

# Export the PFD
with open(PFD_file, "w", newline='') as out_file:
    PFD_csv = csv.writer(out_file)
    for entry in PFD:
        PFD_csv.writerow(entry)
