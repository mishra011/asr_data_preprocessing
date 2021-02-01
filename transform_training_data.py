import os
from os import listdir, getcwd, walk
from os.path import isfile, join, abspath
import json
import random
import librosa

#/dacx/CompressedAudioTransfer_upto_26jan
base_dir = "CompressedAudioTransfer_upto_26jan"

#current_dir = abspath(getcwd())
current_dir = "/dacx"
print(current_dir)


sub_dir_list = listdir(join(current_dir, base_dir))

print(sub_dir_list)
print()

##########################################
def read_transcript_to_dict(filename):
    #print(filename)
    rr = open(filename, "r")
    data = rr.read()
    data = json.loads(data)
    return data

######################################

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

def splitter(data):
    train, valid, test = [], [], []
    
    #print(data[0])
    new_data = []
    all_trans = []
    for item in data:
        trans = read_transcript_to_dict(filename=item)['alternatives'][0]['transcript']
        if trans not in all_trans:
            all_trans.append(trans)
            new_data.append(item)
    l = len(new_data)
    print("TOTAL DATA :: ", l)
    #new_data = random.sample(new_data, len(new_data))
    m = [int((l*80)/100), int((l*10)/100)]
    train = new_data[:m[0]]
    valid = new_data[m[0]:m[0]+m[1]]
    test = new_data[m[0]+m[1]:]
    print(len(train), len(valid), len(test), l)

    return (train, valid, test)



#####################################
transcript_file_list = []
for dir in sub_dir_list:
    working_dir = join(current_dir,base_dir, dir)
    #print(working_dir)

    _meta = [join(working_dir, f) for f in listdir(working_dir) if isfile(join(working_dir, f)) and f.endswith('.txt')]
    transcript_file_list += _meta
    #print(transcript_file_list)


print(len(transcript_file_list))
# print(transcript_file_list[:5])



language_based_data = split_on_language(transcript_file_list=transcript_file_list)

languages = list(language_based_data.keys())
print(languages)

DIR = "Full_Data_v4"
parts = ["train", "valid", "test"]



for lang in languages:
    print("LANGUAGE :: ", lang)
    lang_data = language_based_data[lang]
    data = splitter(lang_data)
    #quit()

    for i, _data in enumerate(data):
        label = parts[i]
        destination_dir = join(current_dir, DIR, lang, label)
        date_counter = {}
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        for filepath in _data:
            ff = filepath.split("/")
            fname = ff[-1]
            date = ff[-2]
            _fname = fname.replace(".txt", "")
            cc = "{0}__{1}".format(label, lang)
            #date_counter = {}
            

            duration = librosa.get_duration(filename=filepath.replace(".txt", ".wav"))
            duration = int(duration * 1000)

            if cc not in date_counter:
                date_counter[cc] =1
            else:
                date_counter[cc] += 1

            name = label + "__"+ lang + "__" + str(duration) + "__" + str(date_counter[cc]).zfill(6) + "__8k" 

            os.system("cp {0} {1}".format(filepath, join(destination_dir, name+".txt")))
            os.system("cp {0} {1}".format(filepath, join(destination_dir, name+".gl")))
            os.system("cp {0} {1}".format(filepath.replace(".txt", ".wav"), join(destination_dir, name+".wav")))
        




