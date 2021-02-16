import glob, os
import librosa


base_path = "/home/deepak/Comp/asr_data_preprocessing_v2/"

processed_path = base_path + 'test_v1/'


files_path = processed_path

def get_all_durations(files_path):
    os.chdir(files_path)
    count = 0
    in_files = []
    out_files = []
    min_dur = 10000000.0
    max_dur = 0.0
    total_dur = 0.0
    for file in glob.glob(files_path + "*" + ".wav"): #glob.glob("*/*.wav"):
        dur = librosa.get_duration(filename=file)
        count +=1
        total_dur +=dur
        if dur > max_dur:
            max_dur = dur
        if dur < min_dur:
            min_dur = dur
        
    print("TOTAL AUDIO FILES :: ",count )

    return total_dur, max_dur, min_dur


total_dur, max_dur, min_dur = get_all_durations(files_path)

print("DIR PATH :: ", files_path)
print("MIN AUDIO LEN IN SECONDS :: ", min_dur)
print("MAX AUDIO LEN IN SECONDS :: ", max_dur)
print("TOTAL AUDIO LEN IN SECONDS :: ", total_dur)

dur_in_hr = total_dur/3600
print("TOTAL AUDIO LEN IN Hours :: ", dur_in_hr)
