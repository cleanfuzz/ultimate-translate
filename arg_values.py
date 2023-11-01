class CliArguments:
    # TODO: Добавить документацию!
    def __init__(self, debug=None, dest_lang=None, src_lang=None,
                 files=None, sep=None, no_cache=None, no_comfort_output=None,
                 comfort_output_time=None, services_pre_choice=None,
                 tags_to_trans=None):
        self.debug = debug
        self.dest_lang = dest_lang
        self.src_lang = src_lang
        self.files = files
        self.sep = sep
        self.no_cache = no_cache
        self.no_comfort_output = no_comfort_output
        self.comfort_output_time = comfort_output_time
        self.services_pre_choice = services_pre_choice
        self.tags_to_trans = tags_to_trans


arguments = CliArguments()
