import sched
import time
from tkinter import *

from PIL import Image

TESTING = True

if(TESTING):
    import preview as display
    from tkinter import *
    master = Tk()
    # the canvas fits matrix and has a margin of [pixel_spacing] around the border
    w = Canvas(master, width=20 + 16 * 50,
               height=20 + 16 * 50)
    w.pack()
    w.create_rectangle(10, 20, 20, 30, fill="#FFF")
    display.generateDisplay(w, 10, 50, 16, 16)
else:
    import Led_display
    display = Led_display(16, 16)


# try:
    # Relative Path
#    img = Image.open("../web/images/256icon.png")
    # In-place modification
#    img.thumbnail((16, 16))
#    img.save("thumb.png")
# except IOError:
#    pass

#s = sched.scheduler(time.time, time.sleep)


def loop(sc):
    print("Doing stuff...")
    # do your stuff
    s.enter(0.1, 1, loop, (sc,))


#s.enter(0.1, 1, loop, (s,))
# s.run()
