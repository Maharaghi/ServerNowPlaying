# If we need it, we can get MusicObject from here woooo
from musicobject import MusicObject
from os import makedirs, mkdir
from embyparser import EmbyParse
from plexparser import PlexParse
import re


class DataManager:
    _manager = None

    def __init__(self):
        self.music_objects = dict()

        if DataManager._manager is None:
            DataManager._manager = self

    @staticmethod
    def GetManager():
        if not DataManager._manager:
            return DataManager()
        return DataManager._manager

    def ParseRequest(self, request, **kwargs):
        uuids = kwargs.get('uuids')
        ua = request.user_agent.string.split('/')[0]
        print("parse was called with ua {}!".format(ua))

        music_obj = None
        if ua == 'Emby Server':
            music_obj = EmbyParse(request)

        if ua == 'PlexMediaServer':
            music_obj = PlexParse(request) # , self.music_objects)

        if music_obj is None:
            return

        if uuids is not None:
            if music_obj.id not in uuids:
                print('UUID was not in uuid list, filtering!')
                return
            else:
                print('UUID found in filter list, allowing event')

        if music_obj == self.music_objects.get(music_obj.user):
            print("Objects were equal")
            return

        self.PrintMusicObject(music_obj)
        self.OutputMusicObject(music_obj)
        self.music_objects[music_obj.user] = music_obj

    def GetMusicObject(self, user):
        return self.music_objects.get(user)

    def GetMusicObjects(self):
        return list(self.music_objects.items())

    def PrintMusicObject(self, data):
        print("Printing object")
        print("State: {}".format(data['state']))
        print("Track: {}".format(data['track']))
        print("Artists: {}".format(data['artist']))
        print("Album: {}".format(data['album']))

    def OutputMusicObject(self, data):
        print("Writing object")
        uuid = re.sub('[^a-zA-Z0-9]', '', data['id'])
        makedirs(uuid, exist_ok=True)
        self.WriteText('{}/{}.txt'.format(uuid, data['user']), str(data))
        self.WriteText('{}/state.txt'.format(uuid), data['state'])
        self.WriteText('{}/track.txt'.format(uuid), data['track'])
        self.WriteText('{}/artist.txt'.format(uuid), data['artist'])
        self.WriteText('{}/album.txt'.format(uuid), data['album'])
        if(data['image']!=None):
            self.WriteFileStorage('{}/thumb.jpg'.format(uuid), data['image'])

    def WriteText(self, file, data):
        with open(file, 'w') as f:
            f.writelines(data)
    def WriteFileStorage(self, file, filestorage_obj):
        try:
            filestorage_obj.save(file)
            print('thumb.jpg write succeded')
        except:
            print('thumb.jpg write failed')
