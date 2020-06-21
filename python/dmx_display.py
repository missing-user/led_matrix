import sacn

sender = sacn.sACNsender()
sender.start()


def generateDisplay(row, col, destination):
    global universe_count
    universe_count = round(0.5 + (row * col) / 170)  # ceil without math imprt
    print(universe_count, (row * col) / 170)
    for universe in range(1, universe_count + 1):  # start at Universe 1
        sender.activate_output(universe)
        sender[universe].destination = destination

    print('dmx control initialized at IP', destination,
          ' with ', universe_count, 'universes')


def drawPixels(pixelData):
    # reduce the touple list to a simple list
    pixelData = list(sum(pixelData, ()))
    for universe in range(1, universe_count + 1):
        data_segment = pixelData[(universe * 510 - 510):510 * universe]
        sender[universe].dmx_data = tuple(data_segment)


def update():
    pass

# sender.stop()
