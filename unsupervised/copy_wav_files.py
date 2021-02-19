import glob, os
import librosa


base_path = "/home/deepak/Comp/asr_data_preprocessing_v2/"

processed_path = base_path + 'test_v1/'


names = []

files_path = processed_path

new_path = base_path + 'test_filter/'




print("SOURCE PATH :: ", files_path)
print("DESTINATION PATH :: ", new_path)

count = 0

for f in glob.glob(files_path + "*" + ".wav"):
    cmd = "cp {0} {1}".format(f, new_path)
    os.system(cmd)
    count +=1
    print("COUNT :: ", count)
