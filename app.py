from flask.helpers import send_from_directory
from musicobject import MusicObject
from flask import Flask, request, render_template, jsonify
from datamanager import DataManager

from flask.wrappers import Response

app = Flask(__name__)

manager = DataManager()

@app.route('/')
def index():
    users = manager.GetMusicObjects()
    return render_template('index.html', data=users)

@app.route('/thumbnail/<userid>/<path:filename>')
def thumbnails(userid, filename):
    return send_from_directory(userid, filename)

@app.route('/status/<userid>')
def userview(userid):
    music_object = manager.GetMusicObject(userid)
    return render_template('user.html', data=music_object)

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