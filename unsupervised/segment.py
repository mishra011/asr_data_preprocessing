


def get_total_duration(current_index, base_index, segments):
    dur = segments[current_index + base_index][1] - segments[base_index][0]
    print("total_duration :: ", dur)
    return dur


def get_audio_duration(current_index, base_index, segments):
    audio_duration = 0
    index = base_index
    while index <= current_index + base_index:
        audio_duration = audio_duration + segments[index][1] - segments[index][0]
        index += 1
    print("audio_duration :: ", audio_duration)
    return audio_duration

def get_current_duration(current_index, base_index, segments):
    return segments[current_index+base_index][1] - segments[base_index][0]

def audio_finished(current_index, base_index, segment_count):
    finish = False
    
    if current_index + 1 + base_index >= segment_count:
        finish = True
    return finish

def valid_duration(audio_duration, total_duration):
    valid = True
    if audio_duration < 2 or total_duration > 29.5 or total_duration < 10.5:
        valid = False
    
    return valid



def audio_segments(input_list):
    merged_segments = []
    
    #Filter all list items which have audio duration less than 1 second
    segments = list(filter(lambda x: x[1]-x[0] > 1.0, input_list))
    
    print("SEGMENTS :: ",list(segments))

    segment_count = len(segments)
    base_index = 0
    print("Total Segments :: ", segment_count)
    
    while base_index < segment_count:
        print(" ############## Start-", base_index, "###############")
        current_index=0
        total_duration = 0
        audio_duration = 0
        print("BASE SEGMENT :: ", segments[base_index])
        
        print("CURRENT SEGMENT :: ", segments[current_index])

        #current_dur = get_current_duration(current_index, base_index, segments)
        
        while get_current_duration(current_index, base_index, segments) < 11.0:

            if audio_finished(current_index, base_index, segment_count):
                print("AUDIO FINISHED")
                total_duration = -1
                break
            else:
                current_index +=1
                print("UPDATED CURRENT SEGMENT :: ", segments[current_index])
            

        if total_duration < 0:
            print("Exit the file end", total_duration)
            break

        total_duration = get_total_duration(current_index, base_index, segments)

        audio_duration = get_audio_duration(current_index, base_index, segments)

        if valid_duration(audio_duration, total_duration):
            merged_segments.append([segments[base_index][0],segments[base_index+current_index][1]])
            base_index = base_index + current_index + 1
            print("FULL JUMP")
        else:
            base_index = base_index + 1
            print("STEP UP")
    
    print("DONE")
            
        
    return merged_segments
    


out = audio_segments([(0, 4),(4,7),(7,14),(14,15.5), (15.5, 16), (16, 44)]) #,(20,200)])
print(out)

print("===============\n\n")

out = audio_segments([(0, 4),(4,14),(14,16.5), (16.5, 17), (17, 44)]) #,(20,200)])
print(out)


print("===============\n\n")

out = audio_segments([(0, 4),(4,5),(5,14), (14,17),(17,20),(20, 29),(29,41)]) #,(20,200)])
print(out)