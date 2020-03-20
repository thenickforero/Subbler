#!/usr/bin/env python3
from extract_data import extract_audio
from get_upload_link import get_upload_link
from upload_audiofile import upload_audiofile
from init_transcription import init_transcription
from check_job import check_job
from get_transcription_data import get_transcription_data
from group_sentences import get_group_sentences as group_lines
from translate_sentences import translate_sentences
from subtitles_creator import subtitles_maker
from os import remove

[input_language, output_language, filename] = [
    'en-US',
    'es',
    'video.mp4'
]

audioFilename = extract_audio(filename)

upload_data = get_upload_link()
upload_audiofile(audioFilename, upload_data['upload_url'])

job_name = init_transcription(input_language, upload_data['key'])
check_job(job_name)

transcript_data = get_transcription_data(job_name)
grouped_sentences = group_lines(transcript_data)

lang = input_language[0:2]

if lang == output_language:
    subtitles_data = grouped_sentences
else:
    subtitles_data = translate_sentences(grouped_sentences, lang, output_language)

subs_filename = f'{filename[0:-4]}.srt'
subtitles_maker(subs_filename, subtitles_data)
remove(audioFilename)
