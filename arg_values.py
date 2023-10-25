class CliArguments:
    # TODO: Добавить документацию, если класс не будет удален.
    def __init__(self, debug=None, dest_lang=None, src_lang=None,
                 files=None, sep=None, no_cache=None, no_comfort_output=None,
                 comfort_output_time=None):
        self.debug = debug
        self.dest_lang = dest_lang
        self.src_lang = src_lang
        self.files = files
        self.sep = sep
        self.no_cache = no_cache
        self.no_comfort_output = no_comfort_output
        self.comfort_output_time = comfort_output_time


arguments = CliArguments()
