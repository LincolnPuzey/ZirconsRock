from gui.resources import *

BIG_FONT = ('Helvetica', 28)
MEDIUM_FONT = ('Helvetica', 17)
SMALL_FONT = ('Helvetica', 14)
TINY_FONT = ('Helvetica', 12)

BG_COLOUR = '#f5f5f5'
BLACK = '#000000'

ERROR_COLOUR_LIGHT = '#ffafaf'
ERROR_COLOUR_MED = '#ff8989'
ERROR_COLOUR_DARK = '#e22424'

SUCCESS_COLOUR_LIGHT = '#a8ffbc'
SUCCESS_COLOUR_MED = '#6bff8d'
SUCCESS_COLOUR_DARK = '#3b894d'

def initialise_syles():

    s = ttk.Style()
    s.theme_use('default')

    # change the default background colour to BG_COLOUR
    s.configure('.', background=BG_COLOUR)

    # background frame
    s.configure('bg.TFrame')

    # polaroid button
    s.configure('image.TButton', font=MEDIUM_FONT, relief=tk.RAISED, borderwidth=1)

    # normal button
    s.configure('TButton', relief=tk.RAISED, borderwidth=1)

    # title label
    s.configure('title.TLabel', font=BIG_FONT)

    # subtitle label
    s.configure('subtitle.TLabel', font=MEDIUM_FONT)

    # heading label
    s.configure('heading.TLabel', font=SMALL_FONT)

    # tiny label
    s.configure('tiny.TLabel', font=TINY_FONT)

    # filepath label
    s.configure('filepath.TLabel', background='#ffffff')

    # error label
    s.configure('error.TLabel', font=TINY_FONT, foreground=ERROR_COLOUR_DARK)

    # normal label
    s.configure('TLabel', font=SMALL_FONT)

    # listboxes
    s.configure('TListbox', relief=tk.SOLID)

    # entries
    s.configure('TEntry', relief=tk.SOLID, borderwidth=1)
