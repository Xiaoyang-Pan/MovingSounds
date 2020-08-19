#convert mp3 file to wav file
from pydub import AudioSegment

#source and dst music file names
src = 'typewriter.mp3'
dst = 'typewriter.wav'

#import mp3 file and export as a wave file
sound = AudioSegment.from_mp3(src)
sound.export(dst,format = 'wav')
