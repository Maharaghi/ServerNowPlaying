import json
from musicobject import MusicObject

def EmbyParse(request):
        print("Called Emby Parser")
        data = json.loads(request.form['data'])

        event = data['Event']
        item = data['Item']

        print(event)

        # Dump received event data
        # with open(event + '.json', 'w') as f:
        #     json.dump(data, f)

        if item.get('MediaType') != 'Audio':
            return

        state = 'UNKNOWN'
        if (event == 'playback.stop'):
            state = 'Stopped'
        elif (event == 'playback.pause'):
            state = 'Paused'
        elif (event == 'playback.unpause' or event == "playback.start"):
            state = 'Playing'
        else:
            # This is not a state we can handle yet, so just dont update the current state i guess
            return

        artist = item.get('Artist')
        artists = item.get('Artists')
        if artists is not None and len(artists) > 0:
            artist = ", ".join(artists)

        return MusicObject(
            id     = data['User']['Id'],
            user   = data['User']['ConnectUserName'],
            state  = state,
            track  = item.get('Name'),
            artist = artist,
            album  = item.get('Album')
        )