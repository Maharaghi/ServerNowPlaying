class MusicObject:
    def __init__(self, id, user, state, track, artist, album):
        self.id = id
        self.user = user
        self.state = state
        self.track = track
        self.artist = artist
        self.album = album

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