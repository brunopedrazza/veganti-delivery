import sys


class Configs:
    def __init__(self):
        downloads_path = ''
        platform = ''
        self.results_path = '/results'
        if sys.platform == 'win32':
            downloads_path = 'C:/Users/Bruno/Downloads/'
            platform = 'windows'
        else:
            downloads_path = '/Users/Bruno/Downloads/'
            platform = 'macos'
        self.downloads_path = downloads_path
        self.platform = platform
        self.holidays_token = 'cGVkcmF6emFicnVub0BnbWFpbC5jb20maGFzaD04MjUwODkyNA'
