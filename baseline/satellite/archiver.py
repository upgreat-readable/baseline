import os, glob
import zipfile


def get_essays_list(mode: str):
    if mode in ['profacti', 'proocenki', 'proznaniya']:
        path_string = 'files/satellite/' + mode + '/essays'
        return os.listdir(path_string)
    pass


def unzip(mode: str, stage: str):
    possible_modes = ['profacti', 'proocenki', 'proznaniya']
    old_cwd = os.getcwd()
    path_string = ''
    if mode in possible_modes:
        os.chdir("files/satellite/" + mode)
        for file in glob.glob('ds_' + mode + '_' + stage + '_*.zip'):
            path_string = file

        os.chdir(old_cwd)
        if path_string == '':
            raise Exception('Архив не найден. Проверьте содержимое папок profacti, proocenki, proznaniya и уточните '
                            'этап - test, train, final.')
        print('Работаем с архивом - ' + path_string)
        fantasy_zip = zipfile.ZipFile("files/satellite/" + mode + '/' + path_string)
        fantasy_zip.extractall('files/satellite/' + mode)

        fantasy_zip.close()
    else:
        raise Exception('Несуществующий саттелит')
    pass