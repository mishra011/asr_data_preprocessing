import glob, os
import librosa
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import scipy.io.wavfile as wavfile
import random
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

def filtered_files(files_path):
    os.chdir(files_path)
    count = 0
    in_files = []
    # out_files = []
    for file in glob.glob(input_file + "*.wav"):

        if os.path.getsize(file) >10000:
            if librosa.get_duration(filename=file) > 90.0:

                count = count + 1
                # if file.endswith('.wav'):
                in_files.append(file)

    return in_files

in_files = filtered_files(input_file)

in_files[0]
len(in_files)

def segment_file(file, outpath, write_segment = True):
    
    filename = os.path.basename(file)

    print(filename)
    
    [Fs, x] = aIO.read_audio_file(file)
    # print(Fs,x)
    segments = aS.silence_removal(x, Fs, 0.05, 0.05, smooth_window = 1.0, weight = 0.3, plot = False)
    
    filter_segments = []

    filter_segments = list(filter(lambda x: x[1]-x[0] > 3.0 and x[1]-x[0] < 20.0, segments))

    if write_segment:
        for i, s in enumerate(filter_segments):
            # print('Start:',s[0],s[1])
            start_buffer = 2.0 
            end_buffer = 2.0
            
            if (s[0] > 2) :
                #Silence prefix between  1 to 2 second
                random_silence_prefix = random.random()
                start_buffer = s[0] - start_buffer + random_silence_prefix
            else:
                start_buffer = s[0]
            
            end_buffer =s[1] + end_buffer
            
            
            strOut = "{0:}___{1:}_{2:.2f}-{3:.2f}_{4:.2f}.wav".format(filename[0:-4], i, start_buffer, end_buffer, s[1]-s[0])
            #print(strOut)
            try:
                wavfile.write(outpath +  "/" + strOut, Fs, x[int(Fs * start_buffer):int(Fs * end_buffer)])
            except:
                print('Failed', strOut)
    
    return filter_segments

# only_audio = True
def segment_files(files, output_file):
    for file in files:
        segment_file(file, output_file)

segment_files(in_files, output_file)