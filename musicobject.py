# If we use the base64 image->str, then we need this
from base64 import b64encode

class MusicObject:
    def __init__(self, id='', user='', state='', track='', artist='', album='', image=None):
        self.id = id
        self.user = user
        self.state = state
        self.track = track
        self.artist = artist
        self.album = album
        self.image = image

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __eq__(self, o: object) -> bool:
        if o is None:
            return False

        if not isinstance(o, MusicObject):
            return False

        return str(self) == str(o)

    def __str__(self) -> str:
        return str(self.__dict__.copy())

    def to_string(self, include_state=False) -> str:
        albumstr = '- {}'.format(self.album) if self.album is not None else ''
        if include_state:
            return '{state}: {track} | {artist}{albumstr}'.format(state=self.state, track=self.track, artist=self.artist, albumstr=albumstr)
        else:
            return '{track} | {artist}{albumstr}'.format(track=self.track, artist=self.artist, albumstr=albumstr)

    def to_json(self):
        obj = {
            'id': self.id,
            'user': self.user,
            'state': self.state,
            'track': self.track,
            'artist': self.artist,
            'album': self.album
        }

        if self.image:
            # This will set the url to the thumbnail we have saved
            obj['image'] = '/thumbnail/{}/thumb.jpg'.format(self.id)
            # This will send the entire image as base64
            # obj['image'] = 'data:image/jpg;base64,' + b64encode(self.image.getbuffer()).decode()

        return obj
