import curses
import editor
    

#============================================================================
# Core update loop
# ----------------
def run(stdscr):
    e = editor.Editor(stdscr)
    while not e.finished:
        e.update_state()
        e.update_screen()


#============================================================================
# Entry point
# -----------
if __name__ == "__main__":
    curses.wrapper(run)
