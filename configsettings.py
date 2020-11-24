import sys


class Configs:
    def __init__(self):
        downloads_path = ''
        platform = ''
        self.results_path = '/results'
        self.downloads_path = '/sheets/'
        if sys.platform == 'win32':
            platform = 'windows'
        else:
            platform = 'macos'
        self.platform = platform
        self.holidays_token = 'cGVkcmF6emFicnVub0BnbWFpbC5jb20maGFzaD04MjUwODkyNA'
