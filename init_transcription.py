from requests import post
from json import dumps


def init_transcription(originLang, s3key):
    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/start-transcription/'
    params = {
        'key': s3key,
        'lang': originLang,
        'format': 'mp3'
    }

    data = post(url, dumps(params)).json()

    jobName = data['job_name']

    return(jobName)
