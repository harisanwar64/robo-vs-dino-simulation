from flask import Flask, render_template, make_response
from flask_restplus import Api, Resource, reqparse
from simulation import RoboVsDino

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
ns = api.namespace('robo-vs-dino', description='Army of remote-controlled robots to fight the dinosaurs')


@ns.route('/')
class RoboVsDinoStatus(Resource):
    def get(self):

        RoboVsDino().create_grid()
        RoboVsDino().display_grid()
        return make_response(render_template('page.html'))


if __name__ == '__main__':
    app.run()
