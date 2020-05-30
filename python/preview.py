def generateDisplay(window, spacing, size, width, height):
    m_width = height
    m_height = width

    global canvas
    canvas = window
    pixel_size = size
    pixel_spacing = spacing

    for x in range(pixel_spacing, pixel_spacing + m_width * (pixel_size + pixel_spacing), pixel_size + pixel_spacing):
        for y in range(pixel_spacing, pixel_spacing + m_height * (pixel_size + pixel_spacing), pixel_size + pixel_spacing):
            window.create_rectangle(
                y, x, y + pixel_size, x + pixel_size, fill="#FFF")


def drawPixels(pixelData):
    for i in range(len(pixelData)):
        canvas.itemconfig(i + 1, fill=_from_rgb(pixelData[i]))


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def update():
    global canvas
    canvas.update()
