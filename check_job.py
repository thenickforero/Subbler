from requests import post
from time import sleep
from json import dumps


def check_job(job_name):
    params = {'job_name': job_name}
    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/check-transcription/'

    response = post(url, dumps(params)).json()

    if response['response'] != 'COMPLETED':
        sleep(30)
        check_job(job_name)
