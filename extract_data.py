from moviepy.editor import *


def extract_audio(filename):
    video = VideoFileClip(filename)
    audio = video.audio
    outputFilename = f'{filename[0:-4]}.mp3'
    audio.write_audiofile(outputFilename, verbose=False)
    return outputFilename
