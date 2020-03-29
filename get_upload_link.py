"""Module to get an upload url to upload audiofiles to an AWS S3
Bucket.
"""
from json import loads
from requests import get
from requests.exceptions import RequestException
from sys import exit


def get_upload_link():
    """Get an AWS S3 preSignedUrl to upload an audiofile to a S3 Bucket.

    Returns:
        str:  an AWS S3 preSignedUrl where you can upload an audiofile using a
              HTTP PUT Request.
    """

    try:
        url = ('https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/'
               'get-upload-link')

        data = get(url).json()

        return data

    except RequestException as conn_error:
        print(
            'There was a connection error getting the upload link for the '
            'audio file'
        )
        print(conn_error)
        exit(1)
