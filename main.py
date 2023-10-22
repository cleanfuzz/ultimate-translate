# ---------------------------------------------------------------------------------------------------
# ultimate-translate BY cleanfuzz                                                                 ^^^
# 18.10.2023                                                                                      ^^^
# Скрипт на Python, который переведет для Вас все значения YAML-файла.                            ^^^
# Попутно даст Вам выбрать из разных вариантов перевода.                                          ^^^
# ---------------------------------------------------------------------------------------------------



import parse_yaml
import cli_arguments
import tui


if __name__ == "__main__":
    """
    Точка входа в программу.
    """

    # Подготавливаем терминал для работы с ANSI-цветами
    tui.init_term_for_ansi_colors()

    # Получаем аргументы командной строки
    args = cli_arguments.parse_cli_args()

    # Включаем режим отладки по желанию пользователя
    debug = args.debug
    tui.enable_debug_output(debug_enabled=debug)

    # Присваиваем переменным аргументы командной строки
    dest_lang = args.destination_language
    source_lang = args.source_language
    yaml_files = args.files
    separator_string = args.separator

    # Получаем значения по умолчанию в язык назначения перевода и язык файла,
    # если не указаны пользователем
    dest_lang, source_lang = cli_arguments.validate_trans_langs(dest_lang, source_lang)

    # Проверяем, что файлы существуют и их возможно прочитать
    cli_arguments.validate_input_files(yaml_files)

    # Обрабатываем файлы и переводим их
    parse_yaml.manipulate_input_files(yaml_files, dest_lang, source_lang, separator_string)
