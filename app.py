import uuid
import json

from flask import Flask, render_template, send_from_directory
from werkzeug.routing import BaseConverter

from flask_socketio import SocketIO, emit

from projects_handling import ProjectManager, ScopeManager


# Define Flask app and wrap it into SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'KIwTR8ZUNG20UkhrXR0Pv0B9ZZigzQpVVT5KK6FA1M'
socketio = SocketIO(app)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

project_manager = ProjectManager()

@app.route('/')
def send_main():
    """ Simple server of statics """
    return send_from_directory('public', 'index.html')

@app.route('/<regex(".*[^\.js]"):path>')
def send_not_js(path):
    """ Simple server of statics """
    return send_from_directory('public', 'index.html')

@app.route('/<regex(".*\.js"):path>')
def send_js(path):
    """ Simple server of statics """
    return send_from_directory('public', path)



@socketio.on('projects:all:get')
def handle_custom_event():
    """ When received this message, send back all the projects """
    emit('projects:all:get:back', json.dumps(project_manager.get_projects()))


@socketio.on('projects:create')
def handle_project_creation(msg):
    """ When received this message, create a new projects """
    project_name = msg['projectName']
    scope = msg['scope']

    # Create new project (and register it)
    create_result = project_manager.create_project(project_name, scope)

    if create_result["status"] == "success":
        # Send the project back
        emit('projects:create:' + project_name, json.dumps({
            'status': 'success',
            'newProject': create_result["new_project"]
        }))


    else:
        # Error occured
        emit('projects:create:' + project_name, json.dumps({
            'status': 'error',
            'text': create_result["text"]
        }))


@socketio.on('projects:delete:uuid')
def handle_project_creation(msg):
    """ When received this message, delete the project """
    project_uuid = msg

    # Delete new project (and register it)
    delete_result = project_manager.delete_project(project_uuid=project_uuid)

    if delete_result["status"] == "success":
        # Send the success result
        emit('projects:delete:uuid:' + project_uuid, json.dumps({
            'status': 'success'
        }))

    else:
        # Error occured
        emit('projects:delete:uuid:' + project_uuid, json.dumps({
            'status': 'error',
            'text': delete_result["text"]
        }))



scope_manager = ScopeManager()

@socketio.on('scopes:all:get')
def handle_custom_event():
    """ When received this message, send back all the scopes """
    emit('scopes:all:get:back', json.dumps(scope_manager.get_scopes()))


@socketio.on('scopes:create')
def handle_scope_creation(msg):
    """ When received this message, create a new scope """
    hostname = msg['hostname']
    IP = msg['IP']
    projectName = msg['projectName']

    # Create new scope (and register it)
    create_result = scope_manager.create_scope(hostname, IP, projectName)

    if create_result["status"] == "success":
        # Send the scope back
        emit('scopes:create:' + scope_name, json.dumps({
            'status': 'success',
            'newProject': create_result["new_scope"]
        }))


    else:
        # Error occured
        # already_existed_scope = getattr(create_result, 'found_scope', None)

        emit('scopes:create:' + scope_name, json.dumps({
            'status': 'error',
            'text': create_result["text"]
        }))


@socketio.on('scopes:delete:scopeID')
def handle_scope_creation(msg):
    """ When received this message, delete the scope """
    scopeID = msg

    # Delete new scope (and register it)
    delete_result = scope_manager.delete_scope(scopeID=scopeID)

    if delete_result["status"] == "success":
        # Send the success result
        emit('scopes:delete:scopeID:' + scopeID, json.dumps({
            'status': 'success'
        }))

    else:
        # Error occured
        emit('scopes:delete:scopeID:' + scopeID, json.dumps({
            'status': 'error',
            'text': delete_result["text"]
        }))


if __name__ == '__main__':
    socketio.run(app)
