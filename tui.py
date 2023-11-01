import logging
import sys

from rich.console import Console
from rich.logging import RichHandler
import colorama as color
from time import sleep
from arg_values import arguments

console = Console()

err_console = Console(file=sys.stderr)

def init_term_for_ansi_colors():
    """
    Готовим эмулятор терминала для вывода цветного текста.
    """
    color.just_fix_windows_console()


def comfort_output(time: int | None = None, fasten_output: bool | None = False,
                   slow_output: bool | None = False):
    """
    Небольшая функция, чтобы сделать вывод
    более комфортным за счёт задержки между
    блоками сообщений.
    """

    # Присвоение значения по умолчанию.
    if time is None and arguments.comfort_output_time is None:
        milisecs_to_sleep = 500
    elif time is None and arguments.comfort_output_time is not None:
        milisecs_to_sleep = arguments.comfort_output_time
    else:
        milisecs_to_sleep = time

    if fasten_output is True:
        # Превращение целого числа в стотысячные доли секунды (миллисекунды / 100).
        # Для использования в циклах, где отображается очень много информации.
        milisecs_to_sleep = (float(milisecs_to_sleep) / 1000) / 100
    elif slow_output is True:
        # Для использования в важных блоках информации,
        # где необходимо дать пользователю все осмыслить.
        milisecs_to_sleep = (float(milisecs_to_sleep) / 1000) * 3
    else:
        # Превращение целого числа в тысячные доли секунды (миллисекунды).
        milisecs_to_sleep = float(milisecs_to_sleep) / 1000

    # Получение опции, отвечающей за мгновенный вывод текста.
    if arguments.no_comfort_output is False:
        sleep(milisecs_to_sleep)


class DebugOutput:
    def __init__(self, debug_enabled: bool):
        self.debug_enabled = debug_enabled

    def enable_debug_output(self):
        # TODO: задокументировать эту функцию
        if self.debug_enabled is True:
            logging.basicConfig(
                level="NOTSET",
                format="%(message)s",
                datefmt="[%X ]",
                handlers=[RichHandler(rich_tracebacks=True)]
            )


class PrintMessagePrefix:

    # Список доступных цветов можно найти здесь:
    # https://rich.readthedocs.io/en/latest/appendix/colors.html#appendix-colors

    def __init__(self, debug_style, info_style, warn_style, error_style):
        self.debug_style = debug_style
        self.info_style = info_style
        self.warn_style = warn_style
        self.error_style = error_style

    def debug(self) -> None:
        console.print('DEBUG', style=self.debug_style, end='\t')

    def info(self) -> None:
        console.print('INFO', style=self.info_style, end='\t')

    def warn(self) -> None:
        console.print('WARN', style=self.warn_style, end='\t')

    def error(self) -> None:
        console.print('ERROR', style=self.error_style, end='\t')


msg_prefix = PrintMessagePrefix(debug_style='bold chartreuse3', info_style='bold slate_blue3',
                                warn_style='bold gold1', error_style='bold underline deep_pink2')


def print_debug(what_to_print, sep=' ', end='\n', style: str | None = None, highlight=True):
    msg_prefix.debug()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def print_info(what_to_print, sep=' ', end='\n', style: str | None = None, highlight=True):
    msg_prefix.info()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def print_warn(what_to_print, sep=' ', end='\n', style: str | None = None, highlight=True):
    msg_prefix.warn()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def print_error(what_to_print, sep=' ', end='\n', style: str | None = None, highlight=True):
    msg_prefix.error()
    err_console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def rich_print(data_to_print, style='', sep=' ', end='\n', highlight=True, width: int = 110):
    console.print(data_to_print, style=style, sep=sep, end=end, highlight=highlight, width=width)
