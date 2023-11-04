from typing import Any
import yaml_keygen_utf_8
from tui import input

def get_nested_dict_value(dictionary, keys):
    """
    Получить словарь со списком ключей, вернуть значение по цепочке ключей.
    """
    for key in keys:
        dictionary = dictionary[key]
    return dictionary


def get_most_nested_yaml_keys(file_to_read, separator='::') -> list[str]:
    """
    Получить список всех ключей YAML-файла, имеющих только одно значение (максимально вложенные ключи).
    Функция использует библиотеку yaml_keygen с единственной правкой от меня: читает только UTF-8.
    На выходе возвращает список строк, содержащих ключи до максимальной вложенности, через `separator`.
    """
    yaml_key_gen = yaml_keygen_utf_8.YAML()
    yaml_file = yaml_key_gen.read(filename=file_to_read)
    return yaml_key_gen.get_keys(data=yaml_file, sep=separator)


def split_string(string_to_split: str, separator: str) -> list[str]:
    """
    Вернуть строку-аргумент в виде списка.
    Разделитель - параметр `separator`.
    """
    return string_to_split.split(separator)


def get_dict_value_by_string(keys_list, dictionary_to_read) -> Any:
    """
    Вход - список yaml-ключей и словарь.
    Выход - значение в словаре по последовательности ключей.
    """
    return get_nested_dict_value(dictionary=dictionary_to_read, keys=keys_list)


def write_nested_dict_value(dictionary: dict, keys: list[str], value: Any) -> None:
    """
    На входе: словарь со списком ключей и значением,
    которое необходимо записать в словарь по цепочке ключей.
    На выходе: None.
    """
    for count, key in enumerate(keys):
        if count == len(keys) - 1:
            dictionary[key] = value
            break
        dictionary = dictionary[key]
