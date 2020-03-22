from math import floor


def timeFormatter(num, size):
    return str(num).rjust(size, '0')


def time_stamp(time_in_seconds):

    time = float(time_in_seconds)
    hours = floor(time / 60 / 60)
    minutes = floor(time / 60) % 60
    seconds = floor(time - minutes * 60)
    milliseconds = int(str(time).split('.')[1])

    if milliseconds < 10:
        milliseconds *= 100
    else:
        milliseconds *= 10

    stamp = f'{timeFormatter(hours, 2)}:{timeFormatter(minutes, 2)}:{timeFormatter(seconds, 2)},{milliseconds}'

    return stamp


def frame_maker(frame, indicator):
    init_time = frame['init_mark']
    end_time = frame['end_mark']
    line_one = frame['text'][0]

    if len(frame['text']) > 1:
        line_two = frame['text'][1]
    else:
        line_two = ''

    line = f'{indicator}\n{time_stamp(init_time)} --> {time_stamp(end_time)}\n{line_one}\n{line_two}'

    return line


def subtitles_maker(filename, data):
    with open(filename, 'w') as subs_file:
        for i in range(len(data)):
            frame = frame_maker(data[i], i + 1)
            end_line = "\n\n" if i < len(data) else "\n"
            subs_file.write(frame + end_line)
    print('Finished subtitling')
