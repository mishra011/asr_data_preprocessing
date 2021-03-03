import os
import sys
from os import listdir
from os.path import join
import soundfile
import glob

# input_file = sys.argv[1]
# destination_dir = sys.argv[2]

# if not os.path.exists(destination_dir):
#         os.makedirs(destination_dir)
count = 0
destination_dir = "/root/ASR/Data/Speech/Unsupervised/dataset_16k"

tsv_file = open(join(destination_dir, "{0}.tsv".format("combined_tsv_file")), "w")
tsv_file.write(destination_dir + "\n")

for files in glob.glob("/root/ASR/Data/Speech/Unsupervised/dataset/" + "*.wav"):

    wavfile_name = os.path.basename(files)
    new_wav_file_name = join(destination_dir, wavfile_name)

    cmd = "sox {0} -r 16000 -b 16 -c 1 {1}".format(files, new_wav_file_name)
    os.system(cmd)

    frames = soundfile.info(new_wav_file_name).frames

    #os.system("cp {0} {1}".format(join(working_dir, fname+ ".wav"), join(destination_dir, fname+".wav")))
    count +=1
    tsv_file.write(str(wavfile_name) + "\t"+ str(frames) + "\n")
    print(count)

tsv_file.close()
