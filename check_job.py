"""Module to handle the delay of an Transcription Job on AWS Transcribe.
"""
from json import dumps
from requests import post
from requests.exceptions import RequestException
from time import sleep
from sys import exit


def check_job(job_name):
    """Checks if transcription job has finished using its job name.

    If the transcription job hasn't finished it will call itself recursively
    until the job is completed.

    Arguments:
        job_name (str): the job name of the transcription job in AWS
                        Transcribe.
    """

    try:
        params = {'job_name': job_name}
        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'check-transcription/')

        response = post(url, dumps(params)).json()
    except RequestException as conn_error:
        print('There was a connection error checking the transcription job')
        print(conn_error)
        exit(1)

    if response['response'] != 'COMPLETED':
        sleep(30)
        check_job(job_name)
