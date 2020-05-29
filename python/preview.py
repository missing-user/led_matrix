pixels = []


def generateDisplay(window, spacing, size, width, height):
    m_width = height
    m_height = width

    pixel_size = size
    pixel_spacing = spacing

    print(pixel_size)

    for x in range(pixel_spacing, pixel_spacing + m_width * pixel_size, pixel_size):
        for y in range(pixel_spacing, pixel_spacing + m_height * pixel_size, pixel_size):
            window.create_rectangle(
                x, y, x + pixel_size, y + pixel_size, fill="#FFF")


def drawPixels(pixelData):
    for idx, pixel in pixelData:
        w.itemconfig(idx, fill="blue")
        print(pixel)
