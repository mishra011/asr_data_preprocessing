import os
from os import listdir, getcwd, walk
from os.path import isfile, join, abspath
import json
import random
from num2word import replaceInt
import string
import re


base_dir = "FULL"

current_dir = abspath(getcwd())
print(current_dir)


sub_dir_list = listdir("./"+ base_dir)
#sub_dir_list = ['en-in']

print(sub_dir_list)
print()

##########################################
def read_transcript_to_dict(filename):
    rr = open(filename, "r")
    data = rr.read()
    data = json.loads(data)
    return data

######################################

def preprocess_transcript(transcript):
    punt = string.punctuation
    punt = punt.replace("'", "")
    
    transcript = replaceInt(transcript)
    regex = re.compile('[%s]' % re.escape(punt))
    transcript = regex.sub(' ', transcript)
    transcript = re.sub(' +', ' ', transcript)
    transcript = transcript.strip()
    return transcript



#######################################

def split_on_language(transcript_file_list=[], language_based_data={}):
    if not transcript_file_list:
        return language_based_data
    
    for f in transcript_file_list:
        data = read_transcript_to_dict(filename=f)
        #print(data)
        lang = data['languageCode'] 
        if lang not in language_based_data:
            language_based_data[lang] = [f]
        else:
            language_based_data[lang].append(f)


    return language_based_data
#########################################

labels = ["train", "valid", "test"]   #[:1]
exclude = set(string.punctuation)
DIR = "dataset"

tsv_file_name = ""

transcript_file_list = []
for lang in sub_dir_list:
    for label in labels:
        working_dir = join(current_dir,base_dir, lang, label)
        print(working_dir)

        _meta = [f for f in listdir(working_dir) if isfile(join(working_dir, f)) and f.endswith('.txt')]
        destination_dir = join(current_dir, DIR, lang, label)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        tsv_file = open(join(destination_dir, "{0}.tsv".format(label)), "w")
        ltr_file = open(join(destination_dir, "{0}.ltr".format(label)), "w")
        wrd_file = open(join(destination_dir, "{0}.wrd".format(label)), "w")
        for m in _meta:
            fname = m.replace(".txt", "")
            transcript = read_transcript_to_dict(join(working_dir, m))['alternatives'][0]['transcript']

            if transcript:
                transcript = transcript.lower()
                new_transcript = preprocess_transcript(transcript)
                
                #print(transcript)
                #print(new_transcript)
                #new_transcript = ''.join(ch for ch in new_transcript if ch not in exclude)
                splitted = new_transcript.split(" ")
                new2 = "|".join(splitted) + "|"
                new2 = " ".join(list(new2))
                #print(new2)
                #print("================")

                current_wav_file_name = join(working_dir, fname+ ".wav")
                new_wav_file_name = join(destination_dir, fname+".wav").replace("8k", "16k")

                cmd = "sox {0} -r 16000 {1}".format(current_wav_file_name, new_wav_file_name)
                os.system(cmd)


                #os.system("cp {0} {1}".format(join(working_dir, fname+ ".wav"), join(destination_dir, fname+".wav")))
                tsv_file.write(new_wav_file_name + " "+ "111" + "\n")
                ltr_file.write(new2 + "\n")
                wrd_file.write(new_transcript + "\n")

        tsv_file.close()
        ltr_file.close()
        wrd_file.close()


# print(len(transcript_file_list))
# print(transcript_file_list[:5])









