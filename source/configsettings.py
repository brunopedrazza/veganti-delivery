import sys
import glob
import os

methods_dict = {
    'stone': 'Stone',
    'stripe': 'stripe',
    'todos': 'pedidos',
    'dinheiro': 'pedidos',
    'transferencia': 'pedidos'
}


class Configs:
    def __init__(self, method):

        def get_latest_file(method):
            list_of_files = glob.glob(f'{self.downloads_path}*')
            list_of_files = list(
                filter(lambda k: methods_dict[method] in k, list_of_files))
            latest_file = ''
            try:
                latest_file = max(list_of_files, key=os.path.getctime)
            except:
                print(f'Arquivo do {method} não encontrado.')
                sys.exit()
            return latest_file

        downloads_path = ''
        platform = ''

        project_name = 'veganti-delivery'

        path = os.getcwd()
        project_index = path.rfind(project_name)
        bar_index = project_index + len(project_name)

        while path[bar_index] not in '\/':
            bar_index += 1

        path = path[:bar_index]

        self.results_path = f'{path}/results/'
        self.downloads_path = f'{path}/sheets/'

        self.latest_file = get_latest_file(method)

        if sys.platform == 'win32':
            platform = 'windows'
        else:
            platform = 'macos'

        self.platform = platform
        self.holidays_token = 'cGVkcmF6emFicnVub0BnbWFpbC5jb20maGFzaD04MjUwODkyNA'
