import random
import time

import environment as env

import animationChains as animChain
import animations as anim
import colormap as cmap
import effect_list
import sph

row = env.rows
col = env.cols


def to8bitRgb(floatList):
    return [(int(i[0] * 255), int(i[1] * 255), int(i[2] * 255)) for i in floatList]


start_time_seconds = time.time()
effects = effect_list.Effect_List()
effects_seg = effect_list.Effect_List()
color_list = []


def get_time():
    """returns the current song time in 'beats units' and reloads everything when the song is over"""
    global start_time_seconds

    # check if the song is over, load the new playing song analysis and generate effects
    if time.time() - start_time_seconds > sph.total_song_time:
        print('getting new song')
        sph.get_track()
        build_song_effects()

    return sph.time_to_beats(time.time() - start_time_seconds)


def colors(time):
    for i, sect in enumerate(sections_list):
        if time > sect['beat']:
            return (sect['hue1'], sect['hue2'])
    return (sections_list[0]['hue1'], sections_list[0]['hue2'])


sections_list = []
def build_song_effects():
    effects.clear()
    effects_seg.clear()

    global start_time_seconds
    start_time_seconds = time.time() - sph.current_song_time
    random.seed(sph.currentTrack['item']['id'])

    global sections_list
    for sect in sph.results['sections']:
        h1 = random.random()
        h2 = random.random()
        if abs(h1 - h2) < 0.15:
            h2 = (h2 + 0.15) % 1
        sections_list.append({'beat': int(sph.time_to_beats(sect['start'])),
                              'hue1': h1,
                              'hue2': h2})
    sections_list.reverse()

    effects.add(effect_list.timed(random.choice(animChain.reg.all)(), 0))
    for beatIndex in range(len(sph.results['beats'])):
        if not effects.get_current(beatIndex).length>1:
            anim_choice = random.choice(animChain.reg.all)
            effects.add(effect_list.timed(anim_choice(), beatIndex))


    for segment in sph.results['segments']:
        seg_time = sph.time_to_beats(
            segment['start'])
        seg_duration = sph.time_to_beats(
            4 * segment['duration'] + segment['start']) - seg_time
        # print(segment, seg_duration, segment['duration'])
        # there are segments with 'none' as their start time
        # print(segment['loudness_max'])
        if seg_time:
            def eff_factory(d, type):
                ix = 2 + segment['pitches'].index(max(segment['pitches']))
                snow = animChain.snowflake_single_factory(x=ix, y=0)

                def eff_func(t):
                    return snow(t / d, fade=int(3 * d))
                    # return anim.wave(t / d, 1, easing.spikeInQuad) if type else anim.diagonal_wave(t / d)
                return eff_func
            eff = eff_factory(seg_duration, colors(seg_time)[1] > 0.5)
            effects_seg.add(effect_list.timed(eff, seg_time, seg_duration))
    print('effects generated', len(effects.repr()))
    #start looping
    setInterval(loop, 10)



def haveBeenLoaded(arg):
    if results != None:
        clearInterval(hack);
        build_song_effects()
hack = setInterval(haveBeenLoaded, 5)


def map_from_to(x, a=0, b=1, c=0, d=1):
    return (x - a) / (b - a) * (d - c) + c


def loop():
    if results != None:
        curr_effects = effects.get_current(get_time())

        # set preliminary random colors
        (hue1, hue2) = colors(get_time())

        m = curr_effects[0]
        # TODO: change hardcoded pick random color pallete


        if not m:
            m = [0 for i in range(row*col)]
            print('replacement')

        coloredImage = cmap.color_map(m, int(hue1*18))

        # ssome JS code to display
        canvas = document.getElementById("canvas");
        ctx = canvas.getContext("2d");
        imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        for i, color in enumerate(to8bitRgb(coloredImage)):
            imgData.data[i*4 + 0] = color[0];
            imgData.data[i*4 + 1] = color[1];
            imgData.data[i*4 + 2] = color[2];
            imgData.data[i*4+3] = 255;
        ctx.putImageData(imgData, 0, 0);
