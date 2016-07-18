class Processor:

    def note_on(self):
        pass

    def note_off(self):
        pass

    def process_next(self, x, **mod_params):
        raise NotImplementedError