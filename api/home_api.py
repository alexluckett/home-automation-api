from flask import Flask, request
from flask_restful import Resource, Api
from endpoints.energenie_light_control import light_action
from endpoints.lg_shutdown import main


class EnergenieLight(Resource):

    def post(self, light_number):
        light_status = request.form['light_status']

        light_action(light_number, light_status)


class TvState(Resource):

    def post(self, ip_address):
        main(ip_address)


app = Flask(__name__)
api = Api(app)

api.add_resource(EnergenieLight, '/bedroom/light/<int:light_number>/state')
api.add_resource(TvState, '/bedroom/tv/<string:ip_address>/state')


if __name__ == '__main__':
    app.run()