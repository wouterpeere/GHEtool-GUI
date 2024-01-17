"""
script to create the translation class from csv file
"""
from os import system

from pandas import read_csv

from GHEtoolGUI import FOLDER


def main():

    df1 = read_csv(FOLDER.joinpath('Translations.csv'), sep=';', encoding='utf-8')

    file_name = FOLDER.joinpath('gui_classes/translation_class.py')

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('from typing import List\n')
        file.write('class Translations:  # pragma: no cover\n')
        list_of_options = df1["name"].to_list()
        list_of_options.append('languages')
        text = f'__slots__ = {tuple(list_of_options)}'
        file.write(f'\t{text}\n')
        file.write('\tdef __init__(self):\n')
        file.write(f'\t\tself.languages: List[str] = {df1.columns[1:].to_list()}\n')
        for name, translations in zip(df1['name'], df1.iloc[:, 1:].to_numpy()):
            text = f'self.{name}: List[str] = {translations.tolist()}'
            file.write(f'\t\t{text}\n')

    system(f'py -m black --line-length 160 {file_name}')


if __name__ == '__main__':  # pragma: no cover
    main()
