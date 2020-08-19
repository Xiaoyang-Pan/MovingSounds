###########################################################
#                                                         #
#           Playing moving Sound in headphones            #
#                                                         #
#   1.Imported a wave audio file                          #
#   2.Controlled the magnitude of input audio signals     #
#   3.Added a time dealy to the input audio signals       #
#   4.Outputted a wave file with moving sound effects     #
#                                                         #
###########################################################

import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

#import input music wave file
data, samplerate = sf.read('typewriter.wav')

audio_sample = data.shape[0]

#Determine the channel size
if len(data.shape) == 2:
    channels = data.shape[1]
elif len(data.shape) == 1:
    channels = 2
    data = data.reshape(audio_sample,1)
    data = data.repeat(2,1)

#choose the time offset between the left and right sterro sound
#between 0.001% of the number of audio samples read
time_offset = round(1*(10**(-5))*audio_sample)
total_sample = round(2*time_offset+audio_sample)

#Initialize the coefficient matric
left_coe = np.zeros((total_sample,1))
right_coe = np.zeros((total_sample,1))

#Controlled the magnitude of the audio signal respect to its total number of audio samples
ratio = 1.0/audio_sample


#obtain a user input ranged from 1 to 2
#1 means slowest sound moving speed, 2 means fastest sound moving speed.
factor = input("Please enter a number between 1 to 2; it relates to the speed of moving sounds: ")
while True:
    try :
        factor = float(factor)
        
        if factor <1 or factor >2:
            factor = float(input("Your input is invalid. Please enter a number between 1 to 2: "))
        else:
            break
    except:
        factor = input("Your input is invalid. Please enter a number between 1 to 2: ")


#Create a coefficient matrix to controll the magintude of the audio samples
#The songs starts from left moving to right in the beginning, and moving back to the right in the end
for i in range(total_sample):
    if i <= time_offset:
        left_coe[i] = 1-i*ratio*factor
        right_coe[i] = 0
    elif i <=audio_sample/2:
        left_coe[i] = 1-i*ratio*factor
        right_coe[i] = (i-time_offset)*ratio*factor
    elif i <= audio_sample/2+time_offset:
        left_coe[i] = 1-audio_sample/2*ratio*factor
        right_coe[i] = (i-time_offset)*ratio*factor
    elif i <= audio_sample/2+2*time_offset:
        left_coe[i] = 1-audio_sample/2*ratio*factor
        right_coe[i] = audio_sample/2*factor*ratio
    else:
        left_coe[i] = 1-audio_sample/2*ratio*factor + (i-audio_sample/2-2*time_offset)*ratio*factor
        right_coe[i] = audio_sample*factor*ratio-(i-audio_sample/2-2*time_offset)*ratio*factor


new_left = np.zeros((total_sample,1))
new_right = np.zeros((total_sample,1))

#matrix multiplication
def matrix_multiply(coe_matrix,audio_data,start_in,end_in,audio_index,offset):
    return np.multiply(coe_matrix[start_in+offset:end_in+offset,0],audio_data[start_in:end_in,audio_index])


#obtain the moving left and right steroe sounds by multiply the coefficient matrixs with the original values
new_left[0:audio_sample//2,0] = matrix_multiply(left_coe,data,0,audio_sample//2,0,0)
new_left[audio_sample//2:audio_sample//2+2*time_offset,0] = left_coe[audio_sample//2,0]*data[audio_sample//2,0]
new_left[audio_sample//2+2*time_offset:total_sample,0] = matrix_multiply(left_coe,data,audio_sample//2,audio_sample,0,2*time_offset)

new_right[time_offset:audio_sample//2+time_offset,0] = matrix_multiply(right_coe,data,0,audio_sample//2,1,time_offset)
new_right[audio_sample//2+time_offset:audio_sample//2+2*time_offset,0] =right_coe[audio_sample//2+time_offset,0] * data[audio_sample//2,1]
new_right[audio_sample//2+2*time_offset:,0] = matrix_multiply(right_coe,data,audio_sample//2,audio_sample,1,2*time_offset)

#and concatenate two matric and turn into one audio file
#output the result as a wav file
new_song = np.concatenate((new_left[:,0:1],new_right),axis = 1)
sf.write('new_typerwriter.wav',new_song,samplerate)

#play the audio file with moving effects
play_back = AudioSegment.from_wav('new_typerwriter.wav')
play(play_back)
