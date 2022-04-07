from flask import Flask, render_template, make_response, jsonify
from flask_restplus import Api, Resource, reqparse, marshal, abort, fields
from app.simulation import RoboVsDino
from app.storage_util import StorageUtility
from config import SimulationConfig
from enum import Enum
import re
import uuid
import base64

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
ns = api.namespace('webapp', description='Army of remote-controlled robots to fight the dinosaurs')
headers = {'Content-Type': 'text/html'}


# 'R' for Robot and 'D' for Dinosaur, Got Exception 400 (bad request) if provided other than Enum
class Type(Enum):
    R = 'R'
    D = 'D'


class Direction(Enum):
    Up = 'Up'
    Down = 'Down'
    Right = 'Right'
    Left = 'Left'


class RobotVsDinoModel(object):
    # API model for creating entity i.e. robot or dinosaurs
    create_entity = api.model('create_entity', {
        # 'id': fields.String(required=False, description='type identifier', attribute='_id'),
        'type': fields.String(required=True, enum=[x.name for x in Type],
                              description='Type of entity i.e. robot or dinosaur'),
        'x_cord': fields.Integer(required=True, description='x-cord of robot in grid'),
        'y_cord': fields.Integer(required=True, description='y-cord of robot in grid'),
        'direction': fields.String(required=False, enum=[x.name for x in Direction],
                                   description = "required for robot only"),
        'description': fields.String(required=False, description='optional description about robot/dinosaur')
    })


class InstructionModel(object):
    # API model for issue instruction i.e. robot can turn left, turn right, move forward, move backward, and attack
    issue_instruction = api.model('issue_instruction', {
        'x_cord': fields.Integer(required=True, description='x-cord of robot in grid'),
        'y_cord': fields.Integer(required=True, description='y-cord of robot in grid'),
        'direction': fields.String(required=True, enum=[x.name for x in Direction],
                                   description="only robot can modify its direction"),
        'attack': fields.Boolean(required=False, description='attack or only change direction', default=False)
    })


# uuid function credits/source:
# https://stackoverflow.com/questions/43169683/how-to-set-unique-string-primary-key-in-flask-sqlalchemy-for-api-endpoint
def uuid_url64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


@ns.route('/<different_page>')
class OtherPage(Resource):
    @ns.response(404, 'No record found')
    def get(self, different_page):
        """Adding default message (instead of error -> page not found) whenever user access path/page other than a home
        page after http://<domain url>/webapp/. """

        response = make_response('The page: %s unaccessable or not found.' % different_page, 404)
        return response


@ns.route('/')
class RoboVsDinoStatus(Resource):
    @ns.response(200, 'OK success')
    @ns.response(404, 'no record found')
    @ns.response(500, 'internal server error')
    def get(self):

        """After accessing url (with port) the page user will see is home page. Home page resides in template directory
           with name page.html"""

        grid_spots = StorageUtility().read_json(SimulationConfig().JSON_FILE)
        df = RoboVsDino().entities_mapping_to_grid(grid_spots)
        # display result.html with table once url hits http://<domain url>/webapp/
        return make_response(render_template('result.html', table=[df.to_html()]), 200, headers)


@ns.route('/create_entity')
class RoboVsDinoCreateEntity(Resource):
    @api.doc('Create Entity i.e. Robot/Dinosaur')
    @ns.response(201, "Created")
    @ns.response(404, 'no record found')
    @ns.response(500, 'internal server error')
    @ns.expect(RobotVsDinoModel.create_entity, validate=True)
    def post(self):

        """This endpoint provides user to create entity (i.e. robot or dinosaur) to the grid simulation space by take
        required parameters i.e. id, type, x_cord, y_cord, direction. Description is optional. If API validates user
        payload, it return 200 with same payload as output. """
        try:
            payload = marshal(api.payload, RobotVsDinoModel.create_entity)
            id = uuid_url64()
            type = payload['type']
            x_cord = payload['x_cord']
            y_cord = payload['y_cord']
            direction = payload['direction']
            desc = payload.get('description', None)
            result = RoboVsDino().add_entity(id, type, x_cord, y_cord, direction, desc, SimulationConfig().JSON_FILE)
            if result:
                # return same payload as input
                return api.payload
            else:
                return {"message": "Grid spot already reserved or coordinates outside simulation grid"}, 404
        except Exception as e:
            abort(500, str(e), status='some internal api error occurred', statusCode='500')


@ns.route('/robot_instruction')
class IssueRobotInstruction(Resource):
    @api.doc('Issue instruction to Robot (It turn left, turn right, move forward, move backward, and attack)')
    @ns.response(200, "Modified")
    @ns.response(404, 'No record found')
    @ns.response(500, 'internal server error')
    @ns.expect(InstructionModel.issue_instruction, validate=True)
    def put(self):
        """This endpoint takes instruction i.e. change robot direction or attack dinosaur. """

        try:
            payload = marshal(api.payload, InstructionModel.issue_instruction)
            x_cord = payload['x_cord']
            y_cord = payload['y_cord']
            direction = payload.get('direction', '')
            attack = payload.get('attack', False)
            result = RoboVsDino().issue_instruction(x_cord, y_cord, direction, attack, SimulationConfig().JSON_FILE)
            if result:
                # return updated json after removing dinosaur as result of successful attack
                return jsonify(result)
            else:
                return {"message": "No entity exists in provided spot or coordinates outside simulation grid"}, 404
        except Exception as e:
            abort(500, str(e), status='some internal api error occurred', statusCode='500')

    @ns.response(204, "Deleted")
    @ns.response(404, 'No record found')
    @ns.response(500, 'internal server error')
    @ns.expect(InstructionModel.issue_instruction, validate=True)
    def delete(self):
        """This endpoint takes instruction of delete by coordinates."""

        try:
            payload = marshal(api.payload, InstructionModel.issue_instruction)
            entity = {
                'x_cord': payload['x_cord'],
                'y_cord': payload['y_cord']
                }
            result = RoboVsDino().kill_entity(entity, SimulationConfig().JSON_FILE)
            if result:
                # return updated json after removing dinosaur as result of successful attack
                return jsonify(result)
            else:
                return {"message": "No entity exists in provided spot or coordinates outside simulation grid"}, 404
        except Exception as e:
            abort(500, str(e), status='some internal api error occurred', statusCode='500')


if __name__ == '__main__':
    app.run()
