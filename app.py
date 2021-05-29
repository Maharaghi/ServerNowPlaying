from musicobject import MusicObject
from flask import Flask, request
from datamanager import DataManager

from flask.wrappers import Response

app = Flask(__name__)

manager = DataManager()

@app.route('/')
def index():
    return '<p>Invalid route :)</p>'

@app.route('/<user>')
def view(user):
    music_object = manager.GetMusicObject(user)
    if music_object is None or not isinstance(music_object, MusicObject):
        return '<p>No data :(</p>'
    data = []
    data.append('<p>State: {}</p>'.format(music_object.state))
    data.append('<p>Track: {}</p>'.format(music_object.track))
    data.append('<p>Artist: {}</p>'.format(music_object.artist))
    data.append('<p>Album: {}</p>'.format(music_object.album))
    return "\n".join(data)

@app.route('/hook', methods=['POST'])
def hook():
    try:
        print(request.data)
        print(request.files)
        uuids = request.args.getlist('uuid')
        if len(uuids) == 1:
            uuids = comma_separated_params_to_list(uuids[0])
        print(uuids)
        manager.ParseRequest(request, uuids=uuids)
    except Exception as e:
        print(e)
        return Response(status=500)

    return Response(status=200)

def comma_separated_params_to_list(param):
    result = []
    for val in param.split(','):
        if val:
            result.append(val)
    return result