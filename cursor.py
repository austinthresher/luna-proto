from copy import copy
from file import TextPos
#============================================================================
# Cursor state and movement
# ---------------------------------------------------------------------------

#TODO push / pop / mark cursor state for more complex scripting


class Cursor(object):
    def __init__(self, file, y=0, x=0):
        self.pos = TextPos(file, y, x)
        self.pos.correct()
        self.stack = []
        self.marks = {}

    @property
    def file(self): return self.pos.file

    @property
    def y(self): return self.pos.y

    @property
    def x(self): return self.pos.x

    @property
    def is_sof(self):
        return self.x == 0 and self.y == 0

    @property
    def is_eof(self):
        return (not self.file.line_is_valid(self.y+1)
            and not self.file.char_is_valid(self.y, self.x+1))

    @property
    def is_sol(self):
        return self.x == 0

    @property
    def is_eol(self):
        return self.at == '\n'

    @property
    def at(self):
        return self.file.char_at(self.y, self.x)

    @property
    def at_prev(self):
        return self.file.char_at(self.y, self.x-1)

    @property
    def at_next(self):
        return self.file.char_at(self.y, self.x+1)

    def left(self):
        return self.pos.left()

    def right(self):
        return self.pos.right()

    def up(self):
        return self.pos.up()

    def down(self):
        return self.pos.down()

    def push(self):
        self.stack.append(copy(self.pos))

    def pop(self):
        if len(self.stack) > 0:
            self.pos = self.stack.pop()
            self.pos.correct()

    def mark(self, tag):
        self.marks[tag] = copy(self.pos)

    def recall(self, tag):
        if tag in self.marks:
            self.pos = copy(self.marks[tag])
