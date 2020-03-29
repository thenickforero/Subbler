"""Module to handle the creation of .srt subtitles using data previously
formatted using group_sentences.py
"""
from math import floor
from sys import exit


def time_formatter(num, size):
    """Adjust a number to a specific size using padding leading zeroes if
    needed.

    Arguments:
        num (int):  the number that will be formatted.
        size (int): the number of characters need in the string representation
                    of the num.

    Returns:
        str:    the string representation of num with a length of size
                including leading zeroes if its needed.
    """

    return str(num).rjust(size, '0')


def time_stamp(time_in_seconds):
    """Create timestamps in the .srt format according a time in seconds:
    seconds -> hh:mm:ss,mmm (mmm = milliseconds)

    Example:
        174.183 -> 00:02:54,183
        328.92  -> 00:05:28,092
    Arguments:
        time_in_seconds (int): the number of seconds for the timestamp.

    Returns:
        str: the timestamp for a certain moment according to the .srt format.
    """

    time = float(time_in_seconds)
    hours = floor(time / 60 / 60)
    minutes = floor(time / 60) % 60
    seconds = floor(time - minutes * 60)
    milliseconds = int(str(time).split('.')[1])

    stamp = (f'{time_formatter(hours, 2)}:{time_formatter(minutes, 2)}:'
             f'{time_formatter(seconds, 2)},{time_formatter(milliseconds, 3)}')

    return stamp


def frame_maker(frame, indicator):
    """Creates a frame based on a subtitle data in the .srt format:
    subtitle_number
    start_timestamp --> end_timestamp
    text_line
    text_line (optional, depends in the amount of data for every frame)

    Example:
        10
        00:01:46,011 --> 00:02:36,067
        there are subtitle lines of
        only five words per line

    Arguments:
        frame (dict):       a subtitle dict with the data of a subtitle frame.
        indicator (int):    the subtitle number for the frame.

    Returns:
        str: a string that represents a subtitle in the .srt format
    """

    init_time = frame['init_mark']
    end_time = frame['end_mark']
    line_one = frame['text'][0]

    if len(frame['text']) > 1:
        line_two = frame['text'][1]
    else:
        line_two = ''

    line = (f'{indicator}\n{time_stamp(init_time)} --> {time_stamp(end_time)}'
            f'\n{line_one}\n{line_two}')

    return line


def subtitles_maker(filename, data):
    """Saves the subtitles in a .srt formatted file.

    Arguments:
        filename (str): the filename of the subtitles file.
        data (list): the list of subtitles data to make every frame.
    """

    try:
        with open(filename, 'w') as subs_file:
            for i in range(len(data)):
                frame = frame_maker(data[i], i + 1)
                end_line = "\n\n" if i < len(data) - 1 else "\n"
                subs_file.write(frame + end_line)
        print('Finished subtitling')

    except OSError as write_error:
        print('There was a problem writing the subtitles file')
        exit(1)
