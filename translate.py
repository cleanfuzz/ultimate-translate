import os
import sys
import translators_fix as trans
from translators_fix.server import TranslatorError
from tui import rich_print
import colorama as color
import parse_yaml
from tui import print_debug, print_info, print_warn, print_error
from time import sleep


def cache_translators():
    """
    Кеширование сессий библиотеки-переводчика для увеличения скорости работы.
    Опционально.
    """
    _ = trans.preaccelerate_and_speedtest()


def get_all_trans_services():
    """
    Просто вернуть список всех доступных сервисов перевода.
    """
    return str(trans.translators_pool)


def prompt_for_trans_services(current_file):
    """
    Данная функция выводит список всех доступных сервисов перевода.
    Также запрашивает у пользователя строку желаемых сервисов,
    возвращает их в виде списка.
    """
    # TODO: Сделать оператор '*', сделать '> help'

    rich_print(
        f'\nТекущий файл: "{os.path.abspath(current_file)}" \nПожалуйста, выберите сервисы, с помощью которых Вы хотите перевести файл. \nДоступные варианты:\n',
        style='bold blue')
    rich_print(get_all_trans_services(), style='bold cyan', highlight=False, width=80)
    rich_print(
        f'\nВведите сервисы через запятую и пробел ", "; например: alibaba, sysTran, google, deepl \n[cyan]{os.path.abspath(current_file)}>[/cyan] ',
        style='bold green', end='')
    trans_services_list = str(input()).split(', ')
    return trans_services_list


def prompt_for_yaml_tags(yaml_keys, current_file, sep):
    """
    Спросить пользователя про YAML-теги,
    на примере которых он хотел бы сравнить
    варианты переводов разных сервисов.
    Возвращает словарь тегов
    """
    # TODO: Сделать оператор '*', сделать '> help', задокументировать функцию

    rich_print(
        f'\nТекущий файл: "{os.path.abspath(current_file)}" \nПожалуйста, выберите YAML-теги, на примере которых Вы хотели бы выбрать сервис перевода. \nДоступные варианты:\n',
        style='bold blue')
    # Сделать вывод более комфортным за счёт задержки в одну секунду
    sleep(0.5)
    rich_print('[', style='bold cyan', highlight=False)
    for key in yaml_keys:
        sleep(0.005)
        rich_print(f"\t'{key}', ", style='bold cyan', highlight=False)
    rich_print(']', style='bold cyan', highlight=False)
    rich_print(
        f'\nВведите теги через запятую и пробел ", ", тег пишется так же, \nкак он написан в списке тегов выше (но без кавычек!); \nнапример: settings{sep}user{sep}debug_on, runtime{sep}config{sep}color_off, action{sep}do\n[cyan]{os.path.abspath(current_file)}>[/cyan] ',
        style='bold green', end='')
    reference_tags_list = list(input().split(', '))
    print('\n', end='')
    return reference_tags_list


def prompt_for_translation_variants(dest_lang, src_lang, yaml_keys, services, full_yaml_dict, sep, current_file):

    # TODO: Сделать оператор '*', сделать '> help', задокументировать функцию

    # print_info('Пожалуйста, подождите, пока пройдёт процесс кеширования.')
    # print_info('Он необходим для быстрого перевода Ваших данных. Кеширование может занять несколько минут.\n\n')
    #
    # cache_translators()

    for string_key in yaml_keys:
        for service in services:
            yaml_value = parse_yaml.get_dict_value_by_string(
                keys_list=parse_yaml.split_string(string_key, separator=sep),
                dictionary_to_read=full_yaml_dict)

            print_debug(f'string_of_keys = {string_key}')

            rich_print(f'{os.path.abspath(current_file)}> [Текущий сервис перевода: {service.upper()}] >>',
                       style='bold cyan')
            rich_print(f'[[ {string_key} ]]:', style='bold tan underline')
            rich_print(translate_value(yaml_value, dest_lang, src_lang, sep, service) + '\n')


def interactive_choices(destination_language, source_language,
                        separator, most_nested_yaml_keys,
                        current_yaml_file, yaml_dict):
    """
    Вызвать интерактивный интерфейс выбора сервиса - переводчика.
    """
    trans_services = prompt_for_trans_services(current_yaml_file)
    yaml_keys_to_translate = prompt_for_yaml_tags(most_nested_yaml_keys, current_yaml_file, separator)
    prompt_for_translation_variants(destination_language, source_language,
                                    yaml_keys_to_translate,
                                    trans_services, yaml_dict, separator, current_yaml_file)


def translate_value(value_to_translate,
                    destination_language, source_language,
                    separator, translator_service, keys_to_values=None):
    """
    Перевести значение из YAML-файла с помощью библиотеки `Translators`.
    """


    try:
        translated = trans.translate_text(value_to_translate,
                                          translator=translator_service, from_language=source_language,
                                          to_language=destination_language, if_use_preacceleration=False)
    except TranslatorError as Err:
        sys.stderr.write(color.Style.BRIGHT + color.Fore.RED + color.Back.BLACK
                         + '\nОШИБКА В МОДУЛЕ ПЕРЕВОДА!'
                         + '\nПожалуйста, проверьте введённые Вами значения сервисов перевода на корректность!'
                         + '\nПрограмма завершает свою работу.\n'
                         + f'TRANSLATOR_ERROR: {Err}'
                         + color.Style.RESET_ALL)
        sys.exit(2)
    else:
        # foobar_print_translated_yaml(keys=keys_to_values, transed_value=translated, sep=separator)
        return translated



def foobar_print_translated_yaml(keys, transed_value, sep):
    """
    Напечатать ключи и их перевод. Только в целях отладки.
    """
    print_debug(str(keys), end=' ', style='cyan')
    print_debug(sep, end=' ', style='bold green')
    print_debug('\n\t' + transed_value.ljust(40))
