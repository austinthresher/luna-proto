import curses
import text
from cursor import Cursor

#============================================================================
# Class that represents the definitions of text objects
# ---------------------------------------------------------------------------
class TextObject(object):

    def word():
        def find_object_start(c):
            while not c.is_sof and c.at_prev.isalnum():
                c.left()
            return c.pos

        def find_object_end(c):
            while not c.is_eof and not c.is_eol and c.at.isalnum():
                c.right()
            return c.pos

        return TextObject(find_object_start, find_object_end)

    def __init__(
            self,
            find_start=[lambda c : c.pos],
            find_end=[lambda c : c.pos]
            ):
        self.find_start = find_start
        self.find_end = find_end

    def at(self, cursor):
        cursor.push()
        start = self.find_start(cursor)
        cursor.pop()

        cursor.push()
        end = self.find_end(cursor)
        cursor.pop()

        return cursor.file.snip(start, end)


#============================================================================
# Editor state
# ---------------------------------------------------------------------------

class Editor(object):
    def __init__(self, stdscr):
        # Set member values
        self.screen = stdscr
        self.height, self.width = self.screen.getmaxyx()
        self.file = text.TextFile("cursor.py")
        self.quit = False
        self.cursor = Cursor(self.file)
        self.status = ""

        # Set curses to non-blocking input
        self.screen.nodelay(True)
        self.screen.timeout(0)

    def update_state(self):
        c = self.screen.getch()
        if c == -1: return
        if c == curses.KEY_LEFT: self.cursor.left()
        if c == curses.KEY_RIGHT: self.cursor.right()
        if c == curses.KEY_UP: self.cursor.up()
        if c == curses.KEY_DOWN: self.cursor.down()
        if c == ord('q'): self.quit = True
        if c == ord('o'): self.status = TextObject.word().at(self.cursor).text
        if c == ord('l'): self.status = self.file.line(self.cursor.y)
        if c == ord('c'): self.status = self.cursor.at
        if c == ord('p'): self.cursor.push()
        if c == ord('P'): self.cursor.pop()
        if c == ord('w'): self.cursor.next_space()
        if c == ord('W'): self.cursor.prev_space()
        if c == ord('a'): self.cursor.next_letter()
        if c == ord('A'): self.cursor.prev_letter()
        if c == ord('s'): self.cursor.next_symbol()
        if c == ord('S'): self.cursor.prev_symbol()
        if c == ord('d'): self.cursor.next_digit()
        if c == ord('D'): self.cursor.prev_digit()

    def update_screen(self):
        for r in range(self.height-1):
            self.screen.addstr(r, 0, self.file.line(r)[:self.width-1])
        clean_status = ('<' + self.status + '>').replace("\n", "\\n").ljust(self.width-1)
        self.screen.addstr(self.height-1, 0, clean_status, curses.A_REVERSE)
        self.screen.move(self.cursor.y, self.cursor.x)
        self.screen.refresh()

    @property
    def finished(self):
        return self.quit


