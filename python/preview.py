from PIL import Image


def generateDisplay(width, height, window, spacing, size):

    global m_height
    global m_width
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


frames = []
save_to_gif = False


def drawPixels(pixelData):
    for i in range(len(pixelData)):
        canvas.itemconfig(i + 1, fill=_from_rgb(pixelData[i]))

    if save_to_gif:
        new_frame = Image.new('RGB', (m_width, m_height))
        new_frame.putdata(pixelData)
        frames.append(new_frame.quantize())
        if len(frames) % 600 == 0:
            # Save into a GIF file that loops forever
            frames[0].save('anim.gif', format='GIF',
                           append_images=frames[1:], save_all=True, duration=6, loop=0)
            # frames.clear()


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb


def update():
    canvas.update()
