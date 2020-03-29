"""Module that handles the translation of subtitles data to a specific
language.
"""
from json import dumps
from requests import post
from requests.exceptions import RequestException
from sys import exit
from time import sleep


def check_translation(s3key):
    """Check if the translation proccess is completed verifying that the
    translated data exists on an AWS S3 Bucket.

    If the translated data isn't in the AWS S3 Bucket it will call itself
    recursively until it's available.

    Arguments:
        s3key (str): the key of the data in the AWS S3 Bucket.
    """

    try:
        params = {'key': f'{s3key}.json'}
        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'check-translation-finished/')

        response = post(url, dumps(params)).json()

    except RequestException as conn_error:
        print('There was a connection error checking the status'
              'of the translation process')
        print(conn_error)
        exit(1)

    if response['status'] != 'available':
        sleep(30)
        check_translation(s3key)


def trigger_translation(data, input_lang, output_lang):
    """Uploads the subtitles data to an AWS Lambda that will process it using
    AWS Translate.

    Arguments:
        data (dict):        the subtitles data in AWS Transcribe format.
        input_lang (str):   the origin language of the subtitles text.
        output_lang (str):  the desired language for the subtitles text.

    Returns:
        str:    the key to access to the translated data (in JSON Format)
                in an AWS S3 Bucket.
    """

    try:
        params = {
            "data": data,
            'input_lang': input_lang,
            'output_lang': output_lang
        }

        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'translate-subtitles/')

        response = post(url, dumps(params)).json()

        return response['key']

    except RequestException as conn_error:
        print('There was a connection error triggering the translation process'
              'on AWS Translate')
        print(conn_error)
        exit(1)


def translate_sentences(data, input_lang, output_lang):
    """Triggers the translation process and downloads the translated data from
    an AWS S3 Bucket.

    Arguments:
        data (dict):        the subtitles data in AWS Transcribe format.
        input_lang (str):   the origin language of the subtitles text.
        output_lang (str):  the desired language for the subtitles text.

    Returns:
        list: the subtitles data translated in the desired language
    """

    s3key = trigger_translation(data, input_lang, output_lang)

    check_translation(s3key)

    try:
        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'get-translation-data/')
        params = {"key": f'{s3key}.json'}

        response = post(url, dumps(params)).json()
        return response

    except RequestException as conn_error:
        print('There was a connection error downloading the translated'
              'subtitles data from an AWS S3 Bucket')
        print(conn_error)
        exit(1)
