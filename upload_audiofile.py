""""Module to handle the uploading of a file to an AWS S3 Bucket using a
preSignedUrl.
"""
from requests import put
from requests.exceptions import RequestException
from sys import exit


def upload_audiofile(filename, url):
    """Uploads of a file to an AWS S3 Bucket using a
    preSignedUrl on a HTTP PUT Request.

    Arguments:
        filename (str): the filename or path to the video that will be
                        processed, it can be relative or absolute.
        url (str): the AWS S3 Bucket preSignedUrl to upload the file.
    """

    try:
        with open(filename, 'rb') as file:
            response = put(
                url,
                data=file,
                headers={'Content-Type': 'audio/mpeg'}
            )

    except OSError as read_audiofile_error:
        print('There was an error opening the audio file that will be uploaded'
              'to an AWS S3 Bucket')
        print(read_audiofile_error)
        exit(1)
