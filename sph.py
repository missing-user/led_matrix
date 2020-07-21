
total_song_time = 120

def time_to_beats(time_seconds):
    for i, beat in enumerate(results['beats']):
        # if the current timestamp is within a beat in the list
        if time_seconds > beat['start'] and time_seconds <= (beat['start'] + beat['duration']):
            return i + (time_seconds - beat['start']) / beat['duration']

    print('no beat found at', time_seconds)
    return 0

def get_track():
    pass
