import os
from os import listdir, getcwd, walk
from os.path import isfile, join, abspath
import glob
import random

base_path = "/home/deepak/Comp/asr_data_preprocessing_v2/asr_data_preprocessing/"

processed_path = base_path + 'unsupervised/'

destination_dir = base_path + "unsupervised/"

tsv_file = open(join(destination_dir, "{0}.tsv".format("test")), "r")

#tsv_file = open(join(destination_dir, "{0}.tsv".format(label)), "w")

train_tsv_file = open(join(destination_dir, "{0}.tsv".format("train")), "w")
valid_tsv_file = open(join(destination_dir, "{0}.tsv".format("valid")), "w")


lines = tsv_file.readlines()

count = 0

z = None

data = []

for line in lines:
    if count == 0:
        z = line.replace("\n", "")
        print(count, z)
        count +=1
    
    else:
        l = line.replace("\n", "").split(" ")
        m = (l[0], l[-1])
        data.append(m)
        print(count, m)
        count +=1


#print(data)

print(len(data))

x = int( 25.0 *len(data)/100)
print(x)

data = random.sample(data, len(data))

train_tsv_file.write(z+ "\n")
valid_tsv_file.write(z+ "\n")

c = 0
for item in data[:x]:
    valid_tsv_file.write(item[0]+ "\t" + item[1]+ "\n")
    c +=1
    print(c, "VALID")

valid_tsv_file.close()

print()

for item in data[x:]:
    train_tsv_file.write(item[0]+ "\t" + item[1]+ "\n")
    c +=1
    print(c, "TRAIN")

train_tsv_file.close()

print("DONE")


