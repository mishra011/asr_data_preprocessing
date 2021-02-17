import os
from os import listdir, getcwd, walk
from os.path import isfile, join, abspath
import json
import random
from num2word import replaceInt
import string
import re
import soundfile

punt = string.punctuation
punt = punt.replace("'", "")
alphabets = list(string.ascii_lowercase)

def word_cleaner(txt):
    words = [("dont", "don't"),("thats", "that's"),("its", "it's"),("thankyou", "thank you"),
    ("donot", "do not"),("isnt", "isn't"),("lets", "let's"), ("cannot","can not"),("whats","what's")]

    for item in words:
        txt = txt.replace(item[0], item[1])
    return txt

def remove_text_inside_brackets(text, brackets="(){}"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # +1: open, -1: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)

def preprocess_transcript(transcript, punt=punt):
    transcript = remove_text_inside_brackets(transcript)
    transcript = replaceInt(transcript)
    regex = re.compile('[%s]' % re.escape(punt))
    transcript = regex.sub(' ', transcript)
    transcript = re.sub(' +', ' ', transcript)
    transcript = transcript.strip()
    transcript = transcript.replace(" '", "'")
    transcript = word_cleaner(transcript)
    return transcript.lower()


wrd_file = open('/home/mrityunjoy/work/fairseq_fb/clean_libri_lm_raw_data.txt', "w")

# Lines = file1.readlines()
#     Lines = [line.replace("\n","").lower() for line in Lines if line and "\n" in line]
#     for line in Lines:

with open('/home/mrityunjoy/work/fairseq_fb/test_corpus.txt') as fname:
    Lines = fname.readlines()
    Lines = [line.replace("\n","").lower() for line in Lines if line and "\n" in line]
    for texts in Lines:
        
        if texts:
            transcripts = preprocess_transcript(transcript=texts, punt=punt)

            wrd_file.write(transcripts + '\n')

wrd_file.close()
fname.close()