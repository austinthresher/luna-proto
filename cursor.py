#============================================================================
# Cursor state and movement
# ---------------------------------------------------------------------------

#TODO push / pop / mark cursor state for more complex scripting

class Cursor(object):
    def __init__(self, file, y=0, x=0, memory=True):
        self.file = file
        self.line = y
        self.char = x
        # Remember previous x position when on shorter lines
        self.memory = memory
        self.mempos = 0
        self.correct()

    def correct_y(self):
        while not self.file.line_is_valid(self.y) and self.y > 0:
            self.line -= 1

    def correct_x(self):
        while not self.file.char_is_valid(self.y, self.x):
            self.char -= 1

    def correct(self):
        self.correct_y()
        self.correct_x()

    def remember(self):
        self.mempos = self.x

    def recall(self):
        if not self.memory: return
        while self.mempos > self.x and self.file.char_is_valid(self.y, self.x+1):
            self.char += 1

    def left(self):
        if self.file.char_is_valid(self.y, self.x - 1):
            self.char -= 1
            self.remember()
        elif self.file.line_is_valid(self.y - 1):
            self.char = len(self.file.line(self.y-1))
            self.remember()
            self.up()

    def right(self):
        if self.file.char_is_valid(self.y, self.x + 1):
            self.char += 1
            self.remember()
        elif self.file.line_is_valid(self.y + 1):
            self.char = 0
            self.remember()
            self.down()

    def up(self):
        if self.file.line_is_valid(self.y - 1):
            self.line -= 1
            self.recall()
            self.correct()

    def down(self):
        if self.file.line_is_valid(self.y + 1):
            self.line += 1
            self.recall()
            self.correct()

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
        return self.x == len(self.file.line(self.y))

    @property
    def at(self):
        line = self.file.line(self.y)
        if self.x == len(line): return "\n" 
        return self.file.line(self.y)[self.x]

    @property
    def at_prev(self):
        self.left()
        ans = self.at
        self.right()
        return ans

    @property
    def at_next(self):
        self.right()
        ans = self.at
        self.left()
        return ans

    @property
    def x(self): return self.char

    @property
    def y(self): return self.line



