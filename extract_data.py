"""Module that handles the audio extraction of a video.
"""
from moviepy.editor import VideoFileClip
from sys import exit


def extract_audio(filename):
    """Extracts the audio of a video in a mp3 format
    audiofile with the same filename.

    Arguments:
        filename (str): the filename or path to the video that will be
                        processed, it can be relative or absolute.

    Returns:
        str: the filename of the audio file which is the original filename
             with .mp3 extension.
    """

    try:
        video = VideoFileClip(filename)
        audio = video.audio
        outputFilename = f'{filename[0:-4]}.mp3'
        audio.write_audiofile(outputFilename, verbose=False)
        return outputFilename

    except OSError as file_error:
        print('Error missing video file')
        print(file_error)
        exit(1)
