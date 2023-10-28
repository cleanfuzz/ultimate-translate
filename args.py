import os
import sys
import yaml
from tui import DebugOutput, print_debug, print_info, print_error, comfort_output
from arg_values import arguments
from translate import get_working_trans_services
import click


def work_with_cli_args():
    """
    Функция для обработки аргументов командной строки.
    """

    # Получаем аргументы командной строки
    # и задаем максимальную ширину вывода библиотеки click.
    parse_cli_args.main(max_content_width=120, standalone_mode=False)

    if '--help' in sys.argv:
        sys.exit(0)

    # Включаем режим отладки по желанию пользователя.
    debug = DebugOutput(debug_enabled=arguments.debug)
    debug.enable_debug_output()

    # Получаем значения по умолчанию в язык назначения перевода и язык файла,
    # если не указаны пользователем.
    arguments.dest_lang, arguments.src_lang = set_default_trans_langs(arguments.dest_lang,
                                                                      arguments.src_lang)

    # Проверяем, что файлы существуют и их возможно прочитать.
    validate_input_files(arguments.files)

    # Возвращаем экземпляр класса CliArguments со значениями аргументов командной строки.
    return arguments


def get_all_valid_trans_services() -> list[str]:
    # TODO: сделать документацию.
    services_to_try_choices = get_working_trans_services() + ', *'
    symbols_to_remove = [' ', '[', ']', '"', "'"]

    for symbol in symbols_to_remove:
        services_to_try_choices = services_to_try_choices.replace(symbol, '')

    return services_to_try_choices.split(',')


def validate_trans_services_pre_choice(ctx, param, value) -> list[str]:
    # TODO: сделать документацию.
    services = str(value)

    try:
        symbols_to_remove = [' ', '[', ']', '(', ')', '"', "'"]

        for symbol in symbols_to_remove:
            services = services.replace(symbol, '')

        services = services.split(',')
        services.pop(-1)

        for i in range(0, len(services)):
            if services[i] not in get_all_valid_trans_services():
                raise click.BadParameter(
                    str(print_error(f'Некорректный аргумент -S / --services-to-try: {services}!')) +
                    str(print_error(f'Список поддерживаемых значений: \n{get_all_valid_trans_services()}'))
                )

        return services

    except Exception as e:
        raise click.BadParameter(str(e)) from e


# Общее описание проекта.
@click.command(help='Ультимативный перевод Yaml-файла с одного языка на другой',
               epilog='''\nЕсли что-то пошло не так, пожалуйста, создайте issue на GitHub:
               https://github.com/cleanfuzz/ultimate-translate/issues/new''')
# Добавление аргументов командной строки, отвечающих за исходный язык и язык назначения.
# Язык назначения по умолчанию - Русский (реализуется функцией `validate_trans_langs`).
@click.option('-d', '--destination-language',
              type=str, default=None, metavar='<LANG>',
              help='''Строка, обозначающая язык, на который необходимо перевести Yaml-файл. 
              Поддерживаемые языки:
              https://github.com/UlionTse/translators/blob/master/README.md#supported-languages''')
# Язык источника по умолчанию - Английский (реализуется функцией `validate_trans_langs`).
@click.option('-s', '--source-language',
              type=str, default=None, metavar='<LANG>',
              help='''Строка, обозначающая исходный язык Yaml-файла.
              Поддерживаемые языки:
              https://github.com/UlionTse/translators/blob/master/README.md#supported-languages''')
# Опционально: отладочная информация.
@click.option('--debug', is_flag=True, default=False,
              help='Выводить ли отладочную информацию.')
# Определяемый пользователем разделитель строк.
@click.option('--separator', type=str, default='::', metavar='<STRING>',
              help='''Строка, используемая для разделения ключей при отображении YAML-файла.
                   Значение по умолчанию: `::`''')
# Отключить кеширование перевода по желанию пользователя.
@click.option('--no-cache', is_flag=True, default=False,
              help='Отключить кеширование (кеширование ускоряет перевод, но может занимать до 5 минут).')
# Отключить задержку вывода между большими блоками сообщений.
@click.option('--no-comfort-output', is_flag=True, default=False,
              help='Отключить "комфортный" вывод (если опция указана, сообщения выводятся мгновенно).')
# Задержка в миллисекундах между выводами больших блоков сообщений
# (работает, если не указана опция `--no-comfort-output`).
# Допустимые значения: 50 - 5000 миллисекунд.
@click.option('--output-time', '-t', 'comfort_output_time', default=500,
              type=click.IntRange(50, 5000), metavar='<TIME>',
              help='Количество миллисекунд между выводом блоков текста (целое число от 50 до 5000).')
# Список сервисов, перевод которых необходимо отобразить на экране.
@click.option('--services-to-try', '-S', 'services_pre_choice', default=None,
              metavar='SERVICES', multiple=True, type=click.STRING,
              callback=validate_trans_services_pre_choice,
              help=f'''Список сервисов перевода через запятую и пробел, 
                        которые Вы хотели бы опробовать в действии (пример: -S 'google, bing, modernMt'). 
                        Список доступных значений можно получить следующим образом:
                        `python {sys.argv[0]} --services-to-try NOT_EXISTS`). 
                        Примечание: Вы можете ввести эти значения по ходу программы.''')
# Список файлов через пробел, которые нужно перевести.
@click.argument('files', type=click.Path(exists=True), required=True, nargs=-1)
def parse_cli_args(destination_language, source_language, debug,
                   separator, no_cache, no_comfort_output,
                   comfort_output_time, services_pre_choice, files) -> None:
    """
    Эта функция получает аргументы командной строки и проверяет их.
    Это действие происходит через декораторы библиотеки click.
    """

    # Присваиваем значения аргументов командной строки объекту arguments.
    arguments.dest_lang = destination_language
    arguments.src_lang = source_language
    arguments.debug = debug
    arguments.sep = separator
    arguments.no_cache = no_cache
    arguments.no_comfort_output = no_comfort_output
    arguments.comfort_output_time = comfort_output_time
    arguments.services_pre_choice = services_pre_choice
    arguments.files = files



def set_default_trans_langs(dest_lang, source_lang):
    """
    Задаём значения по умолчанию для `--destination-language` и `--source-language`, если не указаны пользователем.
    Также предупреждаем пользователя об отсутствии значений.
    """
    internal_dest_lang = dest_lang
    internal_source_lang = source_lang

    if internal_dest_lang is None:
        internal_dest_lang = 'ru'
        print_info('Вы не указали язык, на который необходимо перевести файл.')
        print_info('Предполагаю, вы хотели перевести файл на русский язык.')
        print_info(
            'Для опции `[green]-d[/green]` '
            '(также известна как `[green]--destination-language[/green]`) '
            'выставлено значение по умолчанию:')
        print_info('Русский язык - "[green]ru[/green]".', highlight=False)
        print_info(
            f'Примечание: полный список аргументов можно посмотреть с помощью '
            f'`[green]python {sys.argv[0]} --help[/green]`.')
        # Сделать вывод более комфортным за счёт задержки
        comfort_output()
        print('\n')

    if internal_source_lang is None:
        internal_source_lang = 'en'
        print_info('Вы не указали исходный язык файла.')
        print_info('Предполагаю, вы хотели перевести файл с английского языка.')
        print_info(
            'Для опции `[green]-s[/green]` '
            '(также известна как `[green]--source-language[/green]`)'
            ' выставлено значение по умолчанию:')
        print_info('Английский язык - "[green]en[/green]".', highlight=False)
        print_info(
            f'Примечание: полный список аргументов можно посмотреть с помощью '
            f'`[green]python {sys.argv[0]} --help[/green]`.')
        comfort_output()
        print('\n')

    return internal_dest_lang, internal_source_lang


def validate_input_files(input_files):
    # TODO: Добавить проверку на пустой файл.
    """
    Данная функция проверяет, возможно ли прочитать файл(ы).
    При первой же неудаче выводит ошибку и выходит с кодом 2.
    """
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            print_info('Проверяю выбранный Вами файл на наличие ошибок.')
            try:
                print_info(f'Полный путь к файлу: "[green]{os.path.abspath(file)}[/green]"', highlight=False)
                yaml.safe_load(f)
            except Exception as exc:
                sys.stderr.write('Ошибка! Не могу прочитать файл!\n')
                sys.stderr.write(f'Название некорректного файла, который вы указали: "{file}"\n')
                sys.stderr.write('Программа завершает работу... (2)\n\n')
                sys.stderr.write(f'ERROR: {str(exc)}')
                sys.exit(2)
            else:
                print_info(f'Ваш файл ("[green]{os.path.abspath(file)}[/green]") может быть прочитан.',
                           style='bold', highlight=False)
            comfort_output()
