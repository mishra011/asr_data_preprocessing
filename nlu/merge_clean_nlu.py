
import os
from os import listdir, getcwd, walk
from os.path import isfile, join, abspath
from num2word import replaceInt
import string
import re
from nltk.tokenize import sent_tokenize


punt = string.punctuation
punt = punt.replace("'", "")
alphabets = list(string.ascii_lowercase)


SOURCE_FOLDER = "txt"

SOURCE_DIR = "/home/deepak/Comp/asr_data_preprocessing_v2/asr_data_preprocessing"  #abspath(getcwd())

working_dir = join(SOURCE_DIR, SOURCE_FOLDER)

print(working_dir)
print(SOURCE_DIR)

final_nlu = open(join(working_dir, "{0}.txt".format("FULL_NLU_CLEANED")), "w")



def check_en(line):
    flag = False
    for alpha in alphabets:
        if alpha in line:
            flag = True
            break
    
    return flag

def remove_non_ascii(text):

    return re.sub(r'[^\x00-\x7F]',' ', text)


def check_hi(line):
    flag = False
    for char in line:
        if ord(u'\u0900') <= ord(char) <= ord(u'\u097F'):
            flag = True
            break
    
    return flag

def remove_text_inside_brackets(text, brackets="(){}"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


def word_cleaner(txt):
    words = [("dont", "don't"),("thats", "that's"),("its", "it's"),("thankyou", "thank you"),
    ("donot", "do not"),("isnt", "isn't"), ("emis", "emi's"), ("atms", "atm's"),
    ("lets", "let's"), ("cannot","can not"),("whats","what's"),
    ("‘", ""), ("’",""), ("“", ""), ("”",""), ("' ", "")]

    for item in words:
        txt = txt.replace(item[0], item[1])
    return txt 


def preprocess_transcript(transcript, lang="en-in", punt=punt):
    transcript = remove_text_inside_brackets(transcript)
    # convert number to text in string
    transcript = replaceInt(transcript)
    # remove roman numeral from string
    transcript = re.sub(r'(?=\b[MCDXLVI]{1,6}\b)M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})', '', transcript.upper()).lower()
    # remove punctuations except "'"
    regex = re.compile('[%s]' % re.escape(punt))
    transcript = regex.sub(' ', transcript)
    transcript = remove_non_ascii(transcript)
    transcript = re.sub(' +', ' ', transcript)
    transcript = transcript.strip()
    transcript = transcript.replace(" '", "'")
    transcript = word_cleaner(transcript)
    return transcript.lower()



files= [join(working_dir, f) for f in listdir(working_dir) if isfile(join(working_dir, f)) and f.endswith('.txt')]



data = []

count = 0

for file in files:
    print("\nREADING FILE :: ",file, "\n")
    file1 = open(file, 'r')
    Lines = file1.readlines()
    Lines = [line.replace("\n","").lower() for line in Lines if line and "\n" in line]
    for line in Lines:
        if line and not check_hi(line) and "##" not in line and "xx" not in line:

            sentences = sent_tokenize(line)

            for sent in sentences:
                sent = preprocess_transcript(sent)
                if sent not in data and len(sent)>1:
                    data.append(sent)
                    final_nlu.write(sent + "\n")
                    count +=1
                    print(count, " :: ",sent)
            

final_nlu.close()





print(len(data))