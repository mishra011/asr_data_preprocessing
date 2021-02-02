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

SOURCE_FOLDER = "Full_Data"

SOURCE_DIR = "/home/deepak/CompressedAudioTransfer_2021-01-26/asr_data_preprocessing_v2"
DESTINATION_DIR = "/home/deepak/CompressedAudioTransfer_2021-01-26/asr_data_preprocessing_v2"
DESTINATION_FOLDER = "dataset"

print("SOURCE_DIR :: ", SOURCE_DIR)
print("SOURCE_FOLDER :: ", SOURCE_FOLDER)
print("DESTINATION_DIR :: ", DESTINATION_DIR)
print("DESTINATION_FOLDER :: ", DESTINATION_FOLDER)



sub_dir_list = listdir(join(SOURCE_DIR, SOURCE_FOLDER))
#sub_dir_list = ['en-in']

print(sub_dir_list)
print()

labels = ["train", "valid", "test"]   #[:1]

##########################################
def read_transcript_to_dict(filename):
    rr = open(filename, "r")
    data = rr.read()
    data = json.loads(data)
    return data

######################################

def preprocess_transcript(transcript, lang="en-in", punt=punt):

    if lang == "en-in":

        transcript = replaceInt(transcript)
        regex = re.compile('[%s]' % re.escape(punt))
        transcript = regex.sub(' ', transcript)
        transcript = re.sub(' +', ' ', transcript)
        transcript = transcript.strip()

    elif lang in ["hi-in", "mr-in"]:
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

def filter_data(transcript, lang="en-in"):
    flag = True
    if lang in ["hi-in", "mr-in"]:
        for alpha in alphabets:
            if alpha in transcript.lower():
                flag = False
                break
    return flag


##########################################


transcript_file_list = []
for lang in sub_dir_list:
    for label in labels:
        working_dir = join(SOURCE_DIR,SOURCE_FOLDER, lang, label)
        print(working_dir)

        _meta = sorted([f for f in listdir(working_dir) if isfile(join(working_dir, f)) and f.endswith('.txt')])
        destination_dir = join(DESTINATION_DIR, DESTINATION_FOLDER, lang, label)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        tsv_file = open(join(destination_dir, "{0}.tsv".format(label)), "w")
        ltr_file = open(join(destination_dir, "{0}.ltr".format(label)), "w")
        wrd_file = open(join(destination_dir, "{0}.wrd".format(label)), "w")
        meta_file = open(join(destination_dir, "{0}.txt".format(label)), "w")
        tsv_file.write(destination_dir + "\n")
        for m in _meta:
            fname = m.replace(".txt", "")
            transcript = read_transcript_to_dict(join(working_dir, m))['alternatives'][0]['transcript']

            if transcript:
                transcript = transcript.lower()
                flag = filter_data(transcript=transcript, lang=lang)
                if flag:
                    new_transcript = preprocess_transcript(transcript=transcript, lang=lang)
                    
                    splitted = new_transcript.split(" ")
                    new2 = "|".join(splitted) + "|"
                    new2 = " ".join(list(new2))
                    

                    current_wav_file_name = join(working_dir, fname+ ".wav")
                    new_wav_file_name = join(destination_dir, fname+".wav").replace("8k", "16k")

                    cmd = "sox {0} -r 16000 {1}".format(current_wav_file_name, new_wav_file_name)
                    os.system(cmd)

                    frames = soundfile.info(new_wav_file_name).frames


                    #os.system("cp {0} {1}".format(join(working_dir, fname+ ".wav"), join(destination_dir, fname+".wav")))
                    tsv_file.write(fname.replace("8k", "16k") + ".wav" + "\t"+ str(frames) + "\n")
                    ltr_file.write(new2 + "\n")
                    meta_file.write(fname.replace("8k", "16k") + ".wav" +"\t" + new_transcript + "\n")
                    wrd_file.write(new_transcript + "\n")

        tsv_file.close()
        ltr_file.close()
        wrd_file.close()
        meta_file.close()


# print(len(transcript_file_list))
# print(transcript_file_list[:5])









