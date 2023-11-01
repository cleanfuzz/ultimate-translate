import os
import random
import sys
from typing import Any
import translators_fix as trans
from translators_fix.server import TranslatorError
from tui import rich_print
import colorama as color
import parse_yaml
from tui import print_debug, print_info, print_warn, print_error
from tui import comfort_output
from arg_values import arguments


class Translations:
    # TODO: Добавить документацию, если класс не будет удален.
    def __init__(self):
        self.print_styles_rand_list = []
        self.styles_list = ['dark_orange3', 'green', 'yellow', 'light_yellow3',
                            'magenta', 'wheat4', 'bright_black', 'sky_blue3',
                            'dark_sea_green3', 'bright_yellow', 'salmon1', 'bright_magenta',
                            'steel_blue3', 'chartreuse4', 'dark_red', 'dark_khaki',
                            'grey23', 'grey39', 'grey54', 'grey70']

    def gen_print_styles(self, num_of_trans_services: int) -> list[str]:
        # sourcery skip: assign-if-exp, min-max-identity, use-fstring-for-concatenation
        if num_of_trans_services <= len(self.styles_list):
            num_of_styles = num_of_trans_services
        else:
            num_of_styles = len(self.styles_list)

        self.print_styles_rand_list = random.sample(self.styles_list, num_of_styles)

        add_to_color = 'italic'
        self.print_styles_rand_list = [style + ' ' + add_to_color for style in self.print_styles_rand_list]
        return self.print_styles_rand_list


translation = Translations()


def cache_translators() -> None:
    """
    Кеширование сессий библиотеки-переводчика для увеличения скорости работы.
    Опционально.
    """
    _ = trans.preaccelerate_and_speedtest()


def get_working_trans_services(get_list: bool | None = False) -> str | list[str]:
    """
    Просто вернуть список всех работающих сервисов перевода.
    """

    # Список неподходящих сервисов:
    # Yandex - устарел API.
    # DeepL - `Unsupported to_language[ru] in ['auto', 'en', 'zh']`.
    # Apertium - не работает перевод на русский язык.
    # Yeekit - `The function yeekit() has been not certified yet.`.
    # Alibaba - `Traceback (most recent call last):...TypeError: 'NoneType' object is not subscriptable`.
    # Argos - `504 Server Error: Gateway Time-out for url: https://translate.argosopentech.com/translate`.
    # Elia - ошибка без текста.
    # Iflytek - `The function iflytek() has been not certified yet.`.
    # Iflyrec - `Unsupported translation: from [en] to [ru]!`.
    # Judic - `Unsupported to_language[ru] in ['de', 'en', 'fr', 'nl'].`.
    # LangugeWire - `Unsupported translation: from [en] to [ru]!`.
    # Lingvanex - `Unsupported to_language[ru] in ['af_ZA', 'am_ET', 'ar_EG', 'ar_SA', 'as_IN', 'az_AZ', 'be_BY',...].`.
    # Niutrans - `The function niutrans() has been not certified yet.`.
    # Mglip - `Unsupported from_language[en] in ['mon', 'xle', 'zh'].`.
    # Mirai - `The function mirai() has been not certified yet.`.
    # MyMemory - `Unsupported to_language[ru] in ['ace-ID', 'acf-LC', 'af-ZA', 'aig-AG', 'ak-GH', 'als-AL',...]`.
    # Tilde - `The function tilde() has been not certified yet.`.
    # TranslateMe - `The function translateMe() has been not certified yet.`.
    # Utibet - `Unsupported from_language[en] in ['ti', 'zh'].`.
    # VolcEngine - `The function volcEngine() has been not certified yet.`.
    # Youdao - `Unsupported translation: from [en] to [ru]!`.

    bad_services = ['apertium', 'alibaba', 'argos', 'deepl',
                    'elia', 'iflyrec', 'iflytek', 'judic',
                    'languageWire', 'lingvanex', 'niutrans',
                    'mglip', 'mirai', 'tilde', 'translateMe',
                    'myMemory', 'utibet', 'yeekit', 'volcEngine',
                    'yandex', 'youdao']

    # Получаем список всех доступных сервисов перевода.
    working_trans_services = trans.translators_pool

    # Убираем 'плохие' сервисы из списка всех.
    for service in bad_services:
        if service in working_trans_services:
            working_trans_services.remove(service)

    if get_list is True:
        return working_trans_services
    else:
        return str(working_trans_services)


def prompt_for_trans_services(current_file: os.PathLike) -> list[str]:
    """
    Данная функция выводит список всех доступных сервисов перевода.
    Также запрашивает у пользователя строку желаемых сервисов,
    возвращает их в виде списка.
    """
    # TODO: Сделать оператор '*', сделать '> help'

    all_working_services = get_working_trans_services(get_list=True)
    # Три случайных сервиса на каждый новый вызов функции.
    rand_services = random.sample(all_working_services, 3)

    # Преобразуем к строкам списки сервисов.
    all_working_services = str(all_working_services)
    rand_services = ', '.join(rand_services)

    rich_print(
        f'\nТекущий файл: "{os.path.abspath(current_file)}" \n'
        f'Пожалуйста, выберите сервисы, с помощью которых Вы хотите перевести файл. \n'
        f'Доступные варианты:\n',
        style='bold blue')
    comfort_output()
    rich_print(all_working_services, style='bold cyan', highlight=False, width=80)
    rich_print(
        f'\nВведите сервисы через запятую и пробел ", "; например: [cyan]{rand_services}[/cyan] \n'
        f'[cyan]{os.path.abspath(current_file)}>[/cyan] ',
        style='bold green', end='')
    if arguments.services_pre_choice is None:
        trans_services_to_test = input().replace(' ', '').split(',')
    else:
        trans_services_to_test = arguments.services_pre_choice
        rich_print(f'Вы ввели следующие значения как аргументы командной строки: \n{trans_services_to_test}')
        comfort_output(slow_output=True)

    if '*' in trans_services_to_test:
        trans_services_to_test = get_working_trans_services(get_list=True)

    return trans_services_to_test


def prompt_for_yaml_tags(yaml_keys: list[str],
                         current_file: str | os.PathLike,
                         sep, file_index: int) -> list[str]:
    """
    Спросить пользователя про YAML-теги,
    на примере которых он хотел бы сравнить
    варианты переводов разных сервисов.
    Возвращает список тегов.
    """
    # TODO: Сделать оператор '*', сделать '> help'

    rich_print(
        f'\nТекущий файл: "{os.path.abspath(current_file)}" \n'
        f'Пожалуйста, выберите YAML-теги, на примере которых Вы хотели бы выбрать сервис перевода. \n'
        f'Доступные варианты:\n',
        style='bold blue')
    # Сделать вывод более комфортным за счёт задержки
    comfort_output()
    rich_print('[', style='bold cyan', highlight=False)
    for key in yaml_keys:
        comfort_output(fasten_output=True)
        rich_print(f"\t{key}, ", style='bold cyan', highlight=False)
    rich_print(']', style='bold cyan', highlight=False)
    rich_print(
        f'\nВведите теги через запятую и пробел ", ", тег пишется так же, \n'
        f'как он написан в списке тегов выше; \n'
        f'например: [cyan]settings{sep}user{sep}debug_on, runtime{sep}config{sep}color_off, action{sep}do[/cyan]\n'
        f'[cyan]{os.path.abspath(current_file)}>[/cyan] ',
        style='bold green', end='')

    if arguments.tags_to_trans is not None and file_index == 0:
        reference_tags_list = arguments.tags_to_trans
        rich_print(f'Вы ввели следующие значения как аргументы командной строки: \n{reference_tags_list}')
        comfort_output(slow_output=True)
    else:
        reference_tags_list = input().replace(' ', '').split(',')
    print('\n', end='')
    return reference_tags_list


def prompt_for_translation_variants(dest_lang: str, src_lang: str, yaml_keys: list,
                                    services: list[str], full_yaml_dict: dict, sep: str,
                                    current_file: os.PathLike,
                                    no_cache: bool, chosen_services: list[str]) -> list[str]:
    # sourcery skip: inline-immediately-returned-variable, simplify-boolean-comparison
    # TODO: Сделать оператор '*', сделать '> help', задокументировать функцию

    # Вызвать процесс кеширования перевода, если не указан ключ командной строки.
    if no_cache is False:
        print_info('Пожалуйста, подождите, пока пройдёт процесс кеширования.')
        print_info('Он необходим для быстрого перевода Ваших данных. Кеширование может занять несколько минут.')
        print_info('Вы можете отключить кеширование с помощью аргумента `[green]--no-cache[/green]`.\n\n')

        cache_translators()

    if len(services) > 5:
        transed_value_style_list = translation.gen_print_styles(len(services))
    else:
        transed_value_style_list = list()
        for i in range(0, len(services)):
            transed_value_style_list.insert(i, '')

    # Напечатать перевод каждого тега в каждом выбранном сервисе перевода.
    # Сначала данный цикл берет тег из списка,
    # затем показывает его во всех вариантах сервисов,
    # выбранных пользователем в функции `prompt_for_trans_services`;
    # затем берет следующий тег, цикл повторяется.
    # Получение строки тегов с разделителем из списка строк YAML-тегов.
    for key_count, string_key in enumerate(yaml_keys):
        # Итерация по списку сервисов перевода, выбранным пользователем.
        for service, transed_value_style in zip(services, transed_value_style_list):
            # Получаем значение из YAML-тега по строке с разделителем.
            yaml_value = parse_yaml.get_dict_value_by_string(
                keys_list=parse_yaml.split_string(string_key, separator=sep),
                dictionary_to_read=full_yaml_dict)

            # PROMPT-LINE.
            rich_print(f'{os.path.abspath(current_file)}> [Текущий сервис перевода: '
                       f'[italic magenta]{service.upper()}[/italic magenta]] >>',
                       style='bold cyan')
            # Вывод списка ключей к текущему тегу.
            rich_print(f'[[ {string_key} ]]:', style='bold tan underline', highlight=False)
            # Вывод перевода текущего тега со случайным стилем.
            rich_print(translate_value(yaml_value, dest_lang, src_lang, sep, service, no_cache) + '\n',
                       style=transed_value_style, highlight=False)

        # Напечатать разделитель, показывающий, что тег переведен всеми выбранными сервисами.
        # Если был переведен последний тег, сказать, что был переведен последний тег.
        if string_key == yaml_keys[-1]:
            print_info(
                f'Последний выбранный Вами тег (№{key_count + 1}, '
                f'{string_key}) переведен всеми выбранными сервисами.',
                highlight=False)
        else:
            print_info(
                f'Тег №{key_count + 1} ({string_key}) переведен всеми выбранными сервисами.',
                highlight=False)
            print_info('Начинаю перевод следующего тега.')
            rich_print('-------------------------------------------------------------------------------------\n',
                       highlight=False)

    # На выходе из цикла спросить желаемый вариант перевода.
    chosen_services = ', '.join(chosen_services)
    rich_print(
        f'\nТекущий файл: "{os.path.abspath(current_file)}" \n'
        f'Пожалуйста, выберите сервисы, результат перевода которых вы хотели бы записать в файл(ы). \n'
        f'Выбранные Вами ранее сервисы:\n',
        style='bold blue')
    rich_print(f'{chosen_services}\n', style='bold cyan', highlight=False, width=80)
    comfort_output()
    print_info('Можно выбрать и тот сервис, перевод которого не был выведен на экран.', highlight=False)
    print_info('Список всех вариантов можно увидеть выше, перед первым выбором сервисов.', highlight=False)
    rich_print(
        f'\nВведите сервисы через запятую и пробел ", ":\n'
        f'[cyan]{os.path.abspath(current_file)}>[/cyan] ',
        style='bold green', end='')

    final_choice_trans_services = input().replace(' ', '').split(',')
    return final_choice_trans_services


def interactive_choices(destination_language: str, source_language: str,
                        separator: str, most_nested_yaml_keys: list[str],
                        current_yaml_file: os.PathLike, yaml_dict: dict, no_cache: bool,
                        file_index: int) -> list[str]:
    """
    Вызвать интерактивный интерфейс выбора сервиса - переводчика.
    """

    trans_services = prompt_for_trans_services(current_yaml_file)
    yaml_keys_to_translate = prompt_for_yaml_tags(most_nested_yaml_keys, current_yaml_file, separator, file_index)
    return prompt_for_translation_variants(destination_language, source_language,
                                           yaml_keys_to_translate, trans_services,
                                           yaml_dict, separator, current_yaml_file,
                                           no_cache, trans_services)


def translate_value(value_to_translate: Any,
                    destination_language: str, source_language: str,
                    separator: str, translator_service: str, no_cache: bool,
                    keys_to_values=None) -> str:
    """
    Перевести значение из YAML-файла с помощью библиотеки `Translators`.
    """

    try:
        translated = trans.translate_text(value_to_translate,
                                          translator=translator_service, from_language=source_language,
                                          to_language=destination_language, if_use_preacceleration=not no_cache)
    except TranslatorError as Err:
        sys.stderr.write(color.Style.BRIGHT + color.Fore.RED + color.Back.BLACK
                         + '\nОШИБКА В МОДУЛЕ ПЕРЕВОДА!'
                         + '\nПожалуйста, проверьте введённые Вами значения сервисов перевода на корректность!'
                         + '\nПрограмма завершает свою работу.\n'
                         + f'TRANSLATOR_ERROR\n {Err}'
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
