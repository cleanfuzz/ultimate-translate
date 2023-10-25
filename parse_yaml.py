import yaml_keygen_utf_8
import yaml
import translate


def get_nested_dict_value(dictionary, keys):
    """
    Получить словарь со списком ключей, вернуть значение по цепочке ключей.
    """
    for key in keys:
        dictionary = dictionary[key]
    return dictionary


def get_most_nested_yaml_keys(file_to_read, separator='::'):
    """
    Получить список всех ключей YAML-файла, имеющих только одно значение (максимально вложенные ключи).
    Функция использует библиотеку yaml_keygen с единственной правкой от меня: читает только UTF-8.
    На выходе возвращает список строк, содержащих ключи до максимальной вложенности, через `separator`.
    """
    yaml_key_gen = yaml_keygen_utf_8.YAML()
    yaml_file = yaml_key_gen.read(filename=file_to_read)
    return yaml_key_gen.get_keys(data=yaml_file, sep=separator)


def split_string(string_to_split, separator):
    """
    Вернуть строку-аргумент в виде списка.
    Разделитель - параметр `separator`.
    """
    return list(string_to_split.split(separator))


def get_dict_value_by_string(keys_list, dictionary_to_read):
    """
    Вход - список yaml-ключей и словарь.
    Выход - значение в словаре по последовательности ключей.
    """
    return get_nested_dict_value(dictionary=dictionary_to_read, keys=keys_list)


def manipulate_input_files(input_files, trans_to, trans_from, sep, disable_caching):
    """
    Выполнить все необходимые действия с файлами:
        Проитерировать список файлов:
            Получить список самых вложенных ключей
            Открыть каждый файл
                Загрузить YAML-файл в память
                и т.д. и т.п.
                [полное описание всех применяемых функций можно посмотреть в их документации]
    """
    for file in input_files:
        yaml_keys_str_list = get_most_nested_yaml_keys(file_to_read=file, separator=sep)

        with open(file, 'r', encoding='utf-8') as f:
            dict_from_yaml = yaml.load(f, Loader=yaml.SafeLoader)

            translate.interactive_choices(destination_language=trans_to, source_language=trans_from,
                                          separator=sep, most_nested_yaml_keys=yaml_keys_str_list,
                                          current_yaml_file=file, yaml_dict=dict_from_yaml, no_cache=disable_caching)

            for string in yaml_keys_str_list:
                yaml_keys_sequence_to_value = split_string(string, separator=sep)
                yaml_value = get_dict_value_by_string(keys_list=yaml_keys_sequence_to_value,
                                                      dictionary_to_read=dict_from_yaml)

                # translate.translate_value(value_to_translate=yaml_value,
                #                           destination_language=trans_to,
                #                           source_language=trans_from, separator=sep,
                #                           keys_to_values=yaml_keys_sequence_to_value)
