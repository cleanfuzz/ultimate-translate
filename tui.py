import logging
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler
import colorama as color

console = Console()


def init_term_for_ansi_colors():
    """
    Готовим эмулятор терминала для вывода цветного текста.
    """
    color.just_fix_windows_console()


def enable_debug_output(debug_enabled: bool = False):
    if debug_enabled == True:
        logging.basicConfig(
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X ]",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
    else:
        pass


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


def print_debug(what_to_print, sep=' ', end='\n', style: Optional[str] = None, highlight=True):
    msg_prefix.debug()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def print_info(what_to_print, sep=' ', end='\n', style: Optional[str] = None, highlight=True):
    msg_prefix.info()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def print_warn(what_to_print, sep=' ', end='\n', style: Optional[str] = None, highlight=True):
    msg_prefix.warn()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def print_error(what_to_print, sep=' ', end='\n', style: Optional[str] = None, highlight=True):
    msg_prefix.error()
    console.print(what_to_print, sep=sep, end=end, style=style, highlight=highlight)


def rich_print(data_to_print, style='', sep=' ', end='\n', highlight=True, width: int = 110):
    console.print(data_to_print, style=style, sep=sep, end=end, highlight=highlight, width=width)
