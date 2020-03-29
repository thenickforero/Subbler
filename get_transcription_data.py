"""Module to download the transcripted data of a video.
"""
from json import dumps
from requests import post
from requests.exceptions import RequestException
from sys import exit


def get_transcription_data(job_name):
    """Downloads from AWS the transcription of a video in a JSON format with
    its text and timestamps using its transcription job name.

    Arguments:
        job_name (str):  the name that identifies the transcription job of a
                         video on AWS Transcribe.

    Returns:
        dict:   a dict with the transcription data (as JSON representation)
                of a video including text and timestamps.
    """

    try:
        params = {'job_name': job_name}
        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'get-subtitles-data/')

        response = post(url, dumps(params)).json()

        return response

    except RequestException as conn_error:
        print('There was a connection error getting the transcription data')
        print(conn_error)
        exit(1)
