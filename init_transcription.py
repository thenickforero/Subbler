"""Module to handle the triggering of the transcription process in AWS
Transcribe.
"""
from json import dumps
from requests import post
from requests.exceptions import RequestException
from sys import exit


def init_transcription(originLang, s3key):
    """Trigger a transcription job on AWS Transcribe of an audiofile in a S3
    Bucket.

    Arguments:
        originLang (str):   the language of voices in the audiofile.
        s3key (str):        the key of the audiofile in the S3 Bucket.

    Returns:
        str:    the job name of the transcription job to track its progress
                and access to its results.
    """

    try:
        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'start-transcription/')
        params = {
            'key': s3key,
            'lang': originLang,
            'format': 'mp3'
        }

        data = post(url, dumps(params)).json()

        jobName = data['job_name']

        return (jobName)

    except RequestException as conn_error:
        print('There was a connection error sending the trigger of the '
              'transcription job')
        print(conn_error)
        exit(1)
