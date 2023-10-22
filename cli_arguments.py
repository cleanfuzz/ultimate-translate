import argparse
import os
import sys
import yaml
from tui import print_debug, print_info, print_warn, print_error


def parse_cli_args():
    """
    Эта функция получает аргументы командной строки и обрабатывает их.
    Также она умеет выводить help по ключу `--help`.
    """
    # Описание проекта.
    parser = argparse.ArgumentParser(description='Ультимативный перевод Yaml-файла с одного языка на другой')

    # Добавление аргументов командной строки, отвечающих за исходный язык и язык назначения.
    # Язык назначения по умолчанию - Русский (реализуется функцией `validate_trans_langs`).
    parser.add_argument('-d', '--destination-language',
                        type=str, default='',
                        help='''Строка, обозначающая язык, на который необходимо перевести Yaml-файл. 
                        Поддерживаемые языки:
                        https://github.com/UlionTse/translators/blob/master/README.md#supported-languages''')

    # Язык источника по умолчанию - Английский (реализуется функцией `validate_trans_langs`).
    parser.add_argument('-s', '--source-language',
                        type=str, default='',
                        help='''Строка, обозначающая исходный язык Yaml-файла. 
                        Поддерживаемые языки: 
                        https://github.com/UlionTse/translators/blob/master/README.md#supported-languages''')

    # Опционально: отладочная информация.
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Выводить ли отладочную информацию.')

    # Определяемый пользователем разделитель строк.
    parser.add_argument('--separator', type=str, default='::', metavar='STRING',
                        help='Строка, используемая для разделения ключей при отображении YAML-файла.')

    # Поменяйте значение `nargs` 1 ==> '+', если необходимо принимать все файлы, предоставленные для перевода.
    parser.add_argument('files', nargs='+', help='Список файлов через пробел, которые нужно перевести.')

    # Проверяем аргументы на ошибки и возвращаем список аргументов.
    cli_args = parser.parse_args()
    return cli_args


def validate_trans_langs(dest_lang, source_lang):
    """
    Задаём значения по умолчанию для `--destination-language` и `--source-language`, если не указаны пользователем.
    Также предупреждаем пользователя об отсутствии значений.
    """
    internal_dest_lang = dest_lang
    internal_source_lang = source_lang

    if internal_dest_lang == '':
        internal_dest_lang = 'ru'
        print_info('Вы не указали язык, на который необходимо перевести файл.')
        print_info('Предполагаю, вы хотели перевести файл на русский язык.')
        print_info(
            'Для опции [green]`-d`[/green] (также известна как [green]`--destination-language`[/green]) выставлено значение по умолчанию:')
        print_info('Русский язык - "ru".')
        print_info(
            f'Примечание: полный список аргументов можно посмотреть с помощью [green]{sys.argv[0]} --help[/green].')
        print('\n')

    if internal_source_lang == '':
        internal_source_lang = 'en'
        print_info('Вы не указали исходный язык файла.')
        print_info('Предполагаю, вы хотели перевести файл с английского языка.')
        print_info(
            'Для опции [green]`-s`[/green] (также известна как [green]`--source-language`[/green]) выставлено значение по умолчанию:')
        print_info('Английский язык - "en".')
        print_info(
            f'Примечание: полный список аргументов можно посмотреть с помощью [green]{sys.argv[0]} --help[/green].')
        print('\n')

    return internal_dest_lang, internal_source_lang


def validate_input_files(input_files):
    """
    Данная функция проверяет, возможно ли прочитать файл(ы).
    При первой же неудаче выводит ошибку и выходит с кодом 2.
    """
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            print_info('Проверяю выбранный Вами файл на наличие ошибок.')
            try:
                print_info(f'Полный путь к файлу: "{os.path.abspath(file)}"')
                yaml.safe_load(f)
            except Exception as exc:
                sys.stderr.write('Ошибка! Не могу прочитать файл!\n')
                sys.stderr.write(f'Название некорректного файла, который вы указали: "{file}"\n')
                sys.stderr.write('Программа завершает работу... (2)\n\n')
                sys.stderr.write('ERROR: ' + str(exc))
                sys.exit(2)
            else:
                print_info(f'Ваш файл ("{os.path.abspath(file)}") может быть прочитан.', style='bold')
