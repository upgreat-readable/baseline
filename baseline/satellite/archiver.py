import os
import zipfile


def get_essays_list(mode: str):
    if mode in ['profacti', 'proocenki', 'proznaniya']:
        path_string = 'files/satellite/' + mode + '/essays'
        return os.listdir(path_string)
    pass


def unzip(mode: str, stage: str):
    if mode in ['profacti', 'proocenki', 'proznaniya']:
        path_string = 'files/satellite/' + mode + '/ds_' + mode + '_' + stage + '.zip'
        fantasy_zip = zipfile.ZipFile(path_string)
        fantasy_zip.extractall('files/satellite/' + mode)

        fantasy_zip.close()
    else:
        raise Exception('Несуществующий саттелит')
    pass