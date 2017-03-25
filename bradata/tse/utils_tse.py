from bradata.utils import _unzip
import os

def unzip_tse(result, current_path):

    if not os.path.exists(current_path + '/data'):
        os.makedirs(current_path + '/data')

    with open(current_path + '/data/temp.zip', 'wb') as f:
        f.write(result)

    _unzip(current_path + '/data/temp.zip', current_path + '/data/')

    os.remove(current_path + '/data/temp.zip')