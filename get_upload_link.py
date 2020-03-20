from requests import get
from json import loads


def get_upload_link():
    url = 'https://cljehyxc6c.execute-api.us-east-1.amazonaws.com/v10/get-upload-link'

    data = get(url).json()

    return data
