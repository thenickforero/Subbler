def chunk_array(array, size):
    result = []
    for i in range(0, len(array), size):
        chunk = array[i:i + size]
        result.append(chunk)
    return result


def get_group_sentences(data):
    stamps = chunk_array(data['data'], 10)
    subtitles = []

    for line in stamps:
        if len(line) > 1:
            first_word = line[0] if line[0]['type'] != 'punctuation' else line[1]
            last_word = line[-1] if line[-1]['type'] != 'punctuation' else line[-2]

            init_mark = first_word['start_time']
            end_mark = last_word['end_time']

            words = []

            for text in line:
                word = text['alternatives'][0]['content']
                words.append(word)

            paragraph = chunk_array(words, 5)
            pre_sentences = [' '.join(line) for line in paragraph]

            sentences = [
                line.replace(' .', '.').replace(' ,', ',')
                for line in pre_sentences
            ]

            subtitles.append(
                {
                    'init_mark': init_mark,
                    'end_mark': end_mark,
                    'text': sentences
                }
            )

    return subtitles
