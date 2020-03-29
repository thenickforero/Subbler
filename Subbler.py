#!/usr/bin/env python3
"""Driver module to use Subbler as an executable script.
"""
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


if __name__ == "__main__":
    """
    You must set in this array the parameters to use subbler according your
    video file.
    """
    [input_language, output_language, filename] = [
        'en-US',
        'es',
        'video.mp4'
    ]

    # Get the audio from the video
    audioFilename = extract_audio(filename)

    # Submit it to an AWS S3 Bucket
    upload_data = get_upload_link()
    upload_audiofile(audioFilename, upload_data['upload_url'])

    # Start the transcription and wait until it's finished
    job_name = init_transcription(input_language, upload_data['key'])
    check_job(job_name)

    # Get the transcription
    transcript_data = get_transcription_data(job_name)

    # Make the subtitles
    grouped_sentences = group_lines(transcript_data)

    """
    If the data doesn't need to be translated don't just pass it to the
    subtitles maker.
    """
    lang = input_language[0:2]
    if lang == output_language:
        subtitles_data = grouped_sentences
    else:
        subtitles_data = translate_sentences(
            grouped_sentences,
            lang,
            output_language
        )

    # Create the subtitles file
    subs_filename = f'{filename[0:-4]}.srt'
    subtitles_maker(subs_filename, subtitles_data)

    # Delete the generated audiofile
    remove(audioFilename)
