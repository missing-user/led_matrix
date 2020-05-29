from PIL import Image

TESTING = True

if(TESTING):
    import preview
    display = preview.Preview_display(16, 16)
else:
    import Led_display
    display = Led_display(16, 16)


try:
    # Relative Path
    img = Image.open("../web/images/256icon.png")
    # In-place modification
    img.thumbnail((16, 16))
    img.save("thumb.png")
    display.drawPixels(range(100))
except IOError:
    pass
