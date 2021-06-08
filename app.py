import argparse
import io
from typing import MutableSequence
from flask.helpers import send_file
from musicobject import MusicObject
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, join_room, namespace, send, emit
from datamanager import DataManager

from flask.wrappers import Response

app = Flask(__name__)
socketio = SocketIO(app)

manager = DataManager()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a webhook server for Emby & Plex servers to expose playback info')
    parser.add_argument(
        '--host',
        metavar='H',
        type=str,
        default='localhost',
        help='The webhook server address'
    )
    parser.add_argument(
        '--port',
        metavar='P',
        type=str,
        default='5000',
        help='The webhook server port'
    )
    args = parser.parse_args()
    socketio.run(app, host=vars(args)['host'], port=vars(args)['port'])


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    emit('message', 'testmessage')


@socketio.on('status')
def handle_status(id):
    obj: MusicObject = manager.GetMusicObject(id)
    if obj:
        obj = obj.to_json()
    emit('status', obj)


@socketio.on('join')
def handle_join(id):
    join_room(id)
    emit('join', id)


def send_status(id, data):
    socketio.emit('status', data, room=id)


@app.route('/')
def index():
    users = manager.GetMusicObjects()
    return render_template('index.html', data=users)


@app.route('/thumbnail/<userid>/<path:filename>')
def thumbnails(userid, filename):
    thumb = io.BytesIO(manager.GetMusicObject(userid).image.getbuffer())
    return send_file(thumb, mimetype='image/jpg')
    # return send_from_directory(userid, filename)


@app.route('/status/<userid>')
def userview(userid):
    music_object = manager.GetMusicObject(userid)
    return render_template('user.html', data=music_object)

@app.route('/status/<userid>/<item>')
def partialview(userid, item):
    music_object = manager.GetMusicObject(userid)
    # Uncomment this if you want to render the original page (with all data) if the target attribute doesn't exist
    # if item is None or (not hasattr(music_object, item) and item != "image"):
    #     return render_template('user.html', data=music_object)
    return render_template('partial.html', data=music_object)

# @app.route('/status/<userid>')
# def userview(userid):
#     music_object = manager.GetMusicObject(userid)
#     return render_template('user.html', data=music_object)


@app.route('/api/status/<userid>')
def statusapi(userid):
    data: MusicObject = manager.GetMusicObject(userid)
    if data is None:
        return Response(status=200)
    return jsonify(data.to_json())


@app.route('/hook', methods=['POST'])
def hook():
    try:
        uuids = request.args.getlist('uuid')
        if len(uuids) == 1:
            uuids = comma_separated_params_to_list(uuids[0])
        musicobj = manager.ParseRequest(request, uuids=uuids)
        if musicobj is not None:
            send_status(musicobj.id, musicobj.to_json())
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
