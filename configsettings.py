import sys

class Configs:
    def __init__(self):
        downloads_path = ''
        platform = ''
        self.results_path = 'C:/Users/Bruno/Code/veganti-delivery/results/'
        if sys.platform == 'win32':
            downloads_path = 'C:/Users/Bruno/Downloads/'
            platform = 'windows'
        else:
            downloads_path = '/Users/Bruno/Downloads/'
            platform = 'macos'
        self.downloads_path = downloads_path
        self.platform = platform