from requests import put


def upload_audiofile(filename, url):
    with open(filename, 'rb') as file:
        response = put(url, data=file, headers={'Content-Type': 'audio/mpeg'})
