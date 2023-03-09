from plover.formatting import OutputHelper

class GameMode:
    def __init__(self, engine):
        self.engine = engine

    def _flush(self):
        if len(self.before.replaced_text) > len(self.after.replaced_text):
            assert self.before.replaced_text.endswith(self.after.replaced_text)
            replaced_text = self.before.replaced_text
        else:
            assert self.after.replaced_text.endswith(self.before.replaced_text)
            replaced_text = self.after.replaced_text
        before = replaced_text[:len(replaced_text)-len(self.before.replaced_text)] + self.before.appended_text
        after = replaced_text[:len(replaced_text)-len(self.after.replaced_text)] + self.after.appended_text
        # common_length = len(commonprefix([before, after]))
        common_length = 0
        erased = len(before) - common_length
        if erased:
            self.output.send_backspaces(erased)
        appended = after[common_length:]
        if appended:
            self.output.send_string(appended)
        self.before.reset(self.after.trailing_space)
        self.after.reset(self.after.trailing_space)

    def _render(self):
        # Render undone actions, ignoring non-text actions.
        for action in self.before.render(undo, last_action):
            pass
        # Render new actions.
        for action in self.after.render(do, last_action):
            self.flush()
            if action.combo:
                self.output.send_key_combination(action.combo)
            elif action.command:
                self.output.send_engine_command(action.command)
        self.flush()

    def start(self):
        self._old_flush = OutputHelper.flush
        self._old_render = OutputHelper.render
        OutputHelper.flush = self._flush
        OutputHelper.render = self._render

    def stop(self):
        OutputHelper.flush = self._old_flush
        OutputHelper.render = self._old_render
