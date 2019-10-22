from copy import copy
from text import TextPos
#============================================================================
# Cursor state and movement
# ---------------------------------------------------------------------------


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

    def right_while(self, condition):
        while not self.is_eof and condition(self):
            self.right()

    def left_while(self, condition):
        while not self.is_sof and condition(self):
            self.left()

    def do_while(self, condition, action):
        action(self)
        while condition(self):
            action(self)

    def next_space(self):
        self.right_while(lambda c : c.at.isspace())
        self.right_while(lambda c : not c.at.isspace())

    def prev_space(self):
        self.left_while(lambda c : c.at.isspace())
        self.left_while(lambda c : not c.at.isspace())

    def next_letter(self):
        self.right_while(lambda c : c.at.isalpha())
        self.right_while(lambda c : not c.at.isalpha())

    def prev_letter(self):
        self.left_while(lambda c : c.at.isalpha())
        self.left_while(lambda c : not c.at.isalpha())

    def next_symbol(self):
        self.right_while(lambda c : not c.at.isalnum() and not c.at.isspace())
        self.right_while(lambda c : c.at.isalnum() or c.at.isspace())

    def prev_symbol(self):
        self.left_while(lambda c : not c.at.isalnum() and not c.at.isspace())
        self.left_while(lambda c : c.at.isalnum() or c.at.isspace())

    def next_digit(self):
        self.right_while(lambda c : c.at.isdigit())
        self.right_while(lambda c : not c.at.isdigit())

    def prev_digit(self):
        self.left_while(lambda c : c.at.isdigit())
        self.left_while(lambda c : not c.at.isdigit())

