import os
import json
import yaml


class DataProvider:

    @staticmethod
    def get(name: str, path: str = '', partition: str = None, extension: str = 'yaml'):
        path = path.replace('/', os.sep)
        file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', path, f'{name}.{extension}'))

        if extension in ['yaml', 'json']:
            with open(file_path, encoding='utf-8', mode='r') as file:
                data = yaml.safe_load(file) if extension == 'yaml' else json.load(file)
                return data if not partition else data[partition]
        else:
            raise ValueError('Неизвестный тип данных')
