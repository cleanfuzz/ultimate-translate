# ---------------------------------------------------------------------------------------------------
# ultimate-translate BY cleanfuzz                                                                 ^^^
# 18.10.2023                                                                                      ^^^
# Скрипт на Python, который переведет для Вас все значения YAML-файла.                            ^^^
# Попутно даст Вам выбрать из разных вариантов перевода.                                          ^^^
# ---------------------------------------------------------------------------------------------------
import files
import parse_yaml
import args
import tui


if __name__ == "__main__":
    """
    Точка входа в программу.
    """

    # Подготавливаем терминал для работы с ANSI-цветами
    tui.init_term_for_ansi_colors()

    # Получение и обработка аргументов командной строки
    args.work_with_cli_args()

    # Обрабатываем файлы и переводим их
    files.manipulate_input_files()
