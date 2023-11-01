import yaml
import os
import translate
import tui
from tui import print_debug, print_info, rich_print
from tqdm import tqdm
from parse_yaml import get_most_nested_yaml_keys, split_string, get_dict_value_by_string, write_nested_dict_value
from arg_values import arguments


def manipulate_input_files():
    """
    Выполнить все необходимые действия с файлами:
        Проитерировать список файлов:
            Получить список самых вложенных ключей
            Открыть каждый файл
                Загрузить YAML-файл в память
                и т.д. и т.п.
                [полное описание всех применяемых функций можно посмотреть в их документации]
    """

    args = arguments

    for file_index, file in enumerate(args.files):
        yaml_keys_str_list = get_most_nested_yaml_keys(file_to_read=file, separator=args.sep)

        with open(file, 'r', encoding='utf-8') as f:
            dict_from_yaml = yaml.load(f, Loader=yaml.SafeLoader)

            services_to_files = translate.interactive_choices(destination_language=args.dest_lang,
                                                              source_language=args.src_lang,
                                                              separator=args.sep,
                                                              most_nested_yaml_keys=yaml_keys_str_list,
                                                              current_yaml_file=file, yaml_dict=dict_from_yaml,
                                                              no_cache=args.no_cache, file_index=file_index)

            filename, file_extension = os.path.splitext(os.path.abspath(file))

            for count, service in enumerate(services_to_files):

                translated_yaml_dict = dict_from_yaml

                if file_extension == '':
                    transed_file_full_path = f'{filename}_{service}-ult-trans'
                else:
                    transed_file_full_path = f'{filename}.{service}-ult-trans{file_extension}'

                print_info(f'Текущий файл для записи перевода: "{transed_file_full_path}".')
                print_info(f'Перевод выбранного Вами сервиса "{service}" (№{count + 1}) будет записан в текущий файл.')

                rich_print('\nЕсли вы хотите изменить путь записи к текущей конфигурации, введите путь к файлу:',
                           style='bold green')
                rich_print(
                    f'Текущий сервис перевода: [cyan]{service}[/cyan]\n'
                    f'Текущее название переведенного файла: [cyan]{transed_file_full_path}[/cyan]\n'
                    f'Оригинальный файл: [cyan]{file}[/cyan]\n\n'
                    f'[bold green][[ Путь к файлу (ENTER для значения по умолчанию) ]]>[/bold green] ',
                    style='bold', end='')

                stay_in_loop = True

                while stay_in_loop:

                    input_file_path = input()

                    if input_file_path == '':
                        input_file_path = transed_file_full_path

                    try:
                        with open(rf'{os.path.abspath(input_file_path)}', 'x', encoding='utf-8'):
                            pass

                        if os.stat(rf'{os.path.abspath(input_file_path)}').st_size == 0:
                            os.remove(rf'{os.path.abspath(input_file_path)}')

                        tui.print_debug(input_file_path)
                        transed_file_full_path = rf'{os.path.abspath(input_file_path)}'


                        stay_in_loop = False

                    except Exception as exc:
                        tui.print_error(str(exc))

                with open(transed_file_full_path, 'x', encoding='utf-8') as out_file:


                    for yaml_key in tqdm(yaml_keys_str_list):
                        transed_value = translate.translate_value(
                            get_dict_value_by_string(split_string(yaml_key, args.sep), translated_yaml_dict),
                            destination_language=args.dest_lang,
                            source_language=args.src_lang, separator=args.sep,
                            keys_to_values=yaml_keys_str_list, no_cache=args.no_cache,
                            translator_service=service)
                        write_nested_dict_value(dictionary=translated_yaml_dict, keys=split_string(yaml_key, args.sep),
                                                value=transed_value)

                    yaml.safe_dump(translated_yaml_dict, out_file, default_flow_style=False,
                                   indent=4, sort_keys=False, allow_unicode=True)
