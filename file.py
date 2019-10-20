#============================================================================
# File being edited. Text is stored as a bytearray of characters. We keep
# a list of newline locations to quickly navigate this array.
# ---------------------------------------------------------------------------
class TextFile(object):
    def __init__(self, filename=None):
        if filename is not None:
            self.open(filename)
        else:
            self.contents = [""]
            self.newlines = []

    def open(self, filename):
        with open(filename) as o:
            self.contents = bytearray(o.read().encode())
        self.index_newlines()

    def index_newlines(self):
        self.newlines = []
        n = self.contents.find(ord('\n'))
        while n != -1:
            self.newlines.append(n)
            if n+1 > len(self.contents):
                break
            n = self.contents.find(ord('\n'), n+1)

    def line_is_valid(self, line_idx):
        return line_idx >= 0 and line_idx < len(self.newlines)

    def char_is_valid(self, line_idx, char_idx):
        if not self.line_is_valid(line_idx):
            return False
        if char_idx < 0 or char_idx > len(self.line(line_idx)):
            return False
        return True

    def line(self, line_idx):
        if not self.line_is_valid(line_idx):
            return "~"

        # Determine the index of the first byte of the line
        start = 0
        if line_idx == 0:
            start = 0
        else:
            start = 1+self.newlines[line_idx-1]

        # Determine the index of the last byte of the line
        end = 0
        if line_idx == len(self.newlines)-1:
            end = len(self.contents)
        else:
            end = self.newlines[line_idx]

        return self.contents[start:end].decode()
