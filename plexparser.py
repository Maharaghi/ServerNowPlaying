import json, re, io
from musicobject import MusicObject

def PlexParse(request, objects_db):

    data = json.loads(request.form['payload'])
    if(data['Metadata']['type']!='track'):
        return None

    event = data['event']
    if(event=='media.stop'):
        state = 'Stopped'
    elif(event=='media.pause'):
        state = 'Paused'
    elif(event=='media.play'):
        state = 'Playing'
    elif(event=='media.resume' or event=='media.scrobble'):
        state = 'Resumed'
    else:
        # ignore all other events / don't update the object
        return None

    if('originalTitle' in data['Metadata']):
        artist = data['Metadata']['originalTitle']
    else:
        artist = data['Metadata']['grandparentTitle']

    # grab plex account uuid if possible
    if('thumb' in data['Account']):
        uuid = re.search('https://plex.tv/users/(.*)/avatar',data['Account']['thumb']).string.split('/')[-2]
    else:
        uuid = data['Account']['id']

    if('thumb' in request.files):
        print('Loading new thumbnail')
        image = io.BytesIO(b'')
        request.files['thumb'].save(image)
    else:
        if(uuid not in objects_db or objects_db[uuid]==None):
            image = None
        else:
            image = objects_db[uuid].image

    return MusicObject(
        state  = state,
        track  = data['Metadata']['title'],
        artist = artist,
        album  = data['Metadata']['parentTitle'],
        id     = uuid,
        user   = data['Account']['title'],
        image  = image
    )