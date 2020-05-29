from tkinter import *


class Preview_display:
    """Preview_display is used to visualize effects during production, without connecting a matrix"""

    def __init__(self, width, height):
        super(Preview_display, self).__init__()
        self.m_width = width
        self.m_height = height
        master = Tk()

        pixel_size = 50
        pixel_spacing = 10
        self.pixels = []

        # the canvas fits matrix and has a margin of [pixel_spacing] around the border
        self.w = Canvas(master, width=2 * pixel_spacing + self.m_width * pixel_size,
                        height=2 * pixel_spacing + self.m_height * pixel_size)
        self.w.pack()
        for x in range(pixel_spacing, pixel_spacing + self.m_width * pixel_size, pixel_size):
            for y in range(pixel_spacing, pixel_spacing + self.m_height * pixel_size, pixel_size):
                self.pixels.append(self.w.create_rectangle(
                    x, y, x + pixel_size, y + pixel_size, fill="#FFF"))

    def drawPixels(pixelData):
        for pixel in pixelData:
            self.w.itemconfig(i, fill="blue")
            print(pixel)
