import os
from os import listdir, getcwd, walk
from os.path import isfile, join, abspath


import re

def remove_non_ascii_2(text):

    return re.sub(r'[^\x00-\x7F]',' ', text)


SOURCE_FOLDER = "txt"

SOURCE_DIR = "/home/deepak/Comp/asr_data_preprocessing_v2/asr_data_preprocessing"  #abspath(getcwd())

working_dir = join(SOURCE_DIR, SOURCE_FOLDER)


filename = join(working_dir, "FULL_NLU_CLEANED.txt")

outfilename = join(working_dir, "collection_NLU.lexicons")

lexicons = open(outfilename, 'w')

count = 0

with open(filename) as fname:
    text = fname.read()
    text = remove_non_ascii_2(text)
    #text = text.replace("'"," ")
    lst = list(set(text.split()))
    lst.sort()
    # print(lst)

    
    for word in lst:
        spell = ' '.join(map(str, word))
        if True:
            lex = word + '\t' + spell + ' |'
            count +=1
            print(count , " :: ", word)
            lexicons.write(str(lex) + '\n')



lexicons.close()

print("LEXICONS CREATED")