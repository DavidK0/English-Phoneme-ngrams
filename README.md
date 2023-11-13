# English-Phoneme-ngrams
 The repository lets you make phoneme level ngram model of English. To use it, run `build_PDF.py`, and then pass the output of that into the input of `process_PFD.py`. The first script will download two text files, combine them, and save the result. The second script will build an ngram model out of that.
 
 The two text files are a pronunciation dictionary and a frequecny dictionary. Combining these gives a pronunciation-frequency dictionary (PFD). From that we can make an ngram model. Here is some example output:

wʌtɚmʌðɚ
sɛlʌm
paʊntɚnmʌnd
brɪkjʌŋ
sʌbʌt
dɪskul

And here is how I would probably spell those words:

Whatermother
Selum
Pounternmund
Brikjung
Suhbut
Diskul
