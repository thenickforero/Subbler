"""Module to handle the creation of subtitles based on AWS Transcribe
processed data.
"""
from sys import exit


def chunk_array(array, size):
    """Create a list of sublists of a specific size based on another list.

    Please take in account that if the size is not an exact divisor of the
    original list length, the last sublist of the list will have less elements
    than expected.

    Examples:
        Inexact:
            array: [1,2,3,4,5]
            size: 2
            result: [ [1,2], [3,4], [5] ]
        Exact:
            array: [1,2,3,4]
            size: 2
            result: [ [1,2], [3,4] ]

    Arguments:
        array (list):  the array that will be divided in subarrays of len: size
        size (int):    the size of every subarray in the response list (taking
                       in account the exactness).

    Returns:
        list: a list of sublists of length equal to size based on array.
    """

    result = []
    for i in range(0, len(array), size):
        chunk = array[i:i + size]
        result.append(chunk)
    return result


def get_group_sentences(data):
    """Creates a list of subtitles with 2 lines of 5 words and its timestamps.

    Arguments:
        data (dict): a dict (from a JSON data) with transcription data
                     following the AWS Transcribe format:

        {
            data:[
                    {
                        "start_time": "106.11",
                        "end_time": "106.64",
                        "alternatives": [
                        {
                            "confidence": "1.0",
                            "content": "hi"
                        }
                        ],
                        "type": "pronunciation"
                    }, ...
            ]
        }

    Returns:
        list: a list of subtitles following this format:

        [
            {
                'init_mark': 106.11,
                'end_mark': 156.67,
                'text': [
                    'there are subtitle lines of',
                    'only five words per line'
                ]
            }, ...
        ]
    """

    if not data:
        print("There isn't any transcription data")
        exit(1)

    try:
        stamps = chunk_array(data['data'], 10)
        subtitles = []

        for line in stamps:
            if len(line) > 1:
                # Don't start a line with punctuation symbols.
                if line[0]['type'] != 'punctuation':
                    first_word = line[0]
                else:
                    first_word = line[1]
                # Don't end a line with punctuation symbols.
                if line[-1]['type'] != 'punctuation':
                    last_word = line[-1]
                else:
                    last_word = line[-2]
                # Set timemarks
                init_mark = first_word['start_time']
                end_mark = last_word['end_time']
                # Create a list of words
                words = []
                for text in line:
                    word = text['alternatives'][0]['content']
                    words.append(word)
                # Create two lines of five words
                paragraph = chunk_array(words, 5)
                pre_sentences = [' '.join(line) for line in paragraph]
                # Adjust punctuation symbols.
                sentences = [
                    line.replace(' .', '.').replace(' ,', ',')
                    for line in pre_sentences
                ]
                # Add subtitle to the response list
                subtitles.append(
                    {
                        'init_mark': init_mark,
                        'end_mark': end_mark,
                        'text': sentences
                    }
                )

        return subtitles

    except KeyError:
        print("The transcripted data isn't in the correct format")
        exit(1)
