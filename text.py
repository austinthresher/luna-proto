
#============================================================================
# A position in an open file
# ---------------------------------------------------------------------------
class TextPos(object):
    def __init__(self, file, y, x):
        self.file = file
        self.y = y
        self.x = x
        self.smart_x = x

    def left(self):
        if self.file.char_is_valid(self.y, self.x - 1):
            self.x -= 1
            self.smart_x = self.x
        elif self.file.line_is_valid(self.y - 1):
            self.x = len(self.file.line(self.y-1))
            self.smart_x = self.x
            self.up()

    def right(self):
        if self.file.char_is_valid(self.y, self.x + 1):
            self.x += 1
            self.smart_x = self.x
        elif self.file.line_is_valid(self.y + 1):
            self.x = 0
            self.smart_x = 0
            self.down()

    def up(self):
        if self.file.line_is_valid(self.y - 1):
            self.y -= 1
            self.correct()

    def down(self):
        if self.file.line_is_valid(self.y + 1):
            self.y += 1
            self.correct()

    def correct(self):
        self.y = self.file.nearest_valid_line(self.y)
        while self.smart_x > self.x and self.file.char_is_valid(self.y, self.x+1):
            self.x += 1
        self.x = self.file.nearest_valid_char(self.y, self.x)


class Snippet(object):
    def __init__(self, file, start_idx, end_idx):
        self.file = file
        self.start = start_idx
        self.end = end_idx

    @property
    def text(self):
        return self.file.contents[self.start:self.end]


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
            self.contents = o.read()
        self.cache_newlines()

    def cache_newlines(self):
        self.newlines = []
        n = self.contents.find('\n')
        while n != -1:
            self.newlines.append(n)
            if n+1 > len(self.contents):
                break
            n = self.contents.find('\n', n+1)

    def line_is_valid(self, line_idx):
        return line_idx >= 0 and line_idx < len(self.newlines)

    def char_is_valid(self, line_idx, char_idx):
        if not self.line_is_valid(line_idx):
            return False
        if char_idx < 0 or char_idx > len(self.line(line_idx)):
            return False
        return True

    def line(self, line_idx):
        if not self.line_is_valid(line_idx): return "~"
        start = self.start_of_line(line_idx)
        end = self.end_of_line(line_idx)
        return self.contents[start:end]

    def start_of_line(self, line_idx):
        if line_idx > 0: return 1 + self.newlines[line_idx - 1]
        return 0

    def end_of_line(self, line_idx):
        if line_idx == len(self.newlines) - 1: return len(self.contents)
        return self.newlines[line_idx]

    def char_at(self, line_idx, char_idx):
        if not self.char_is_valid(line_idx, char_idx): return ""
        return self.contents[self.start_of_line(line_idx) + char_idx]

    def snip(self, start_pos, end_pos):
        return Snippet(
                self,
                self.start_of_line(start_pos.y) + start_pos.x,
                self.end_of_line(end_pos.y) + end_pos.x
            )

    def nearest_valid_line(self, line_idx):
        if line_idx < 0: line_idx = 0
        while not self.line_is_valid(line_idx) and line_idx > 0:
            line_idx -= 1
        return line_idx

    def nearest_valid_char(self, line_idx, char_idx):
        if char_idx < 0: char_idx = 0
        while not self.char_is_valid(line_idx, char_idx) and char_idx > 0:
            char_idx -= 1
        return char_idx
 
