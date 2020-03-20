from requests import post
from json import dumps
from time import sleep


def check_transcription(s3key):
    params = {'key': f'{s3key}.json'}
    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/check-translation-finished/'

    response = post(url, dumps(params)).json()

    if response['status'] != 'available':
        sleep(30)
        check_transcription(s3key)


def trigger_translation(data, input_lang, output_lang):
    params = {
        "data": data,
        'input_lang': input_lang,
        'output_lang': output_lang
    }

    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/translate-subtitles/'

    response = post(url, dumps(params)).json()

    return response['key']


def translate_sentences(data, input_lang, output_lang):

    s3key = trigger_translation(data, input_lang, output_lang)

    check_transcription(s3key)

    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/get-translation-data/'
    params = {"key": f'{s3key}.json'}

    response = post(url, dumps(params)).json()
    return response
