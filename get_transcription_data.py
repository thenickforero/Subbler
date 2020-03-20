from requests import post
from json import dumps


def get_transcription_data(job_name):

    params = {'job_name': job_name}
    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/get-subtitles-data/'

    response = post(url, dumps(params)).json()

    return response
