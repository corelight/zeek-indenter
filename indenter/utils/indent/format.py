from .constants import Constants

# adapted from http://lacusveris.com/PythonTidy/PythonTidy-1.22.python
class FormatCode(object):
    def __init__(self, file_out):
        object.__init__(self)
        self.unit = ""
        self.margin = Constants.NULL
        self.newline = "\n"
        self.buffer = Constants.NULL
        self.chunks = None
        self.outfile = file_out
        return

    def close(self):
        self.unit += self.buffer
        with open(self.outfile, 'w') as out:
            out.write(self.unit)
        out.close()
        return self

    def line_init(self, indent=Constants.ZERO):
        self.col = Constants.ZERO
        margin = self.margin + Constants.INDENTATION * indent
        self.tab_stack = []
        self.tab_set(len(margin) + len(Constants.INDENTATION))
        self.chunks = []
        self.line_more(margin)
        return self

    def line_more(self, chunk=Constants.NULL, can_break_after=False):
        self.chunks.append([chunk, can_break_after])
        self.col += len(chunk)
        return self

    def line_term(self):         
        self.pos = Constants.ZERO
        can_break_before = False
        cumulative_width = Constants.ZERO
        chunk_lengths = []
        self.chunks.reverse()
        for (chunk, can_break_after,) in self.chunks:
            if can_break_after:
                cumulative_width = Constants.ZERO
            cumulative_width += len(chunk)
            chunk_lengths.insert(Constants.ZERO, [chunk, cumulative_width, can_break_after,])
        for (chunk, cumulative_width, can_break_after,) in chunk_lengths:
            if ((self.pos + cumulative_width) > Constants.COL_LIMIT and self.pos > Constants.ZERO):
                if can_break_before:
                    self.put('%s' % self.newline)
                    self.pos = self.tab_forward(True)
            self.put(chunk)
            self.pos += len(chunk)
            can_break_before = can_break_after
        self.put(self.newline)
        return self

    def tab_forward(self, flag):
        if len(self.tab_stack) > 1:
            col = (self.tab_stack)[1]
        else:
            col = (self.tab_stack)[Constants.ZERO]
        self.put(Constants.SPACE * col * (1 if flag else -1))
        return col

    def put(self, text):
        self.buffer += text
        if self.buffer.endswith('\n'):
            self.unit += self.buffer
            self.buffer = Constants.NULL
        return self

    def tab_set(self, col):
        if col > Constants.COL_LIMIT / 2:
            if self.tab_stack:
                col = (self.tab_stack)[-1] + Constants.TAB_SIZE
            else:
                col = Constants.TAB_SIZE
        self.tab_stack.append(col)
        return self
