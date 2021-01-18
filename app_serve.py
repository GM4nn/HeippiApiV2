from flask import Flask,request
from flask_restful import Resource, Api, marshal_with
from app.models_instance import exSql
from app.models import Usuarios
from app.forms import CreateUserForm
from app.resources import usuarios,autentificacion,sistema,actualizar_password,medicos_registros,brindar_especialidades_paciente,usuario
from config.config import DevelopmentConfig
from flask_jwt_extended import JWTManager
import wtforms_json

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
jwt = JWTManager(app)
api = Api(app)
exSql.db.init_app(app)
wtforms_json.init()
base_url = "/api/v1"

api.add_resource(usuarios,"{}/Usuarios".format(base_url))
api.add_resource(autentificacion,"{}/auth".format(base_url))
api.add_resource(sistema,"{}/Sistema".format(base_url))
api.add_resource(actualizar_password,"{}/ActualizarContraseña".format(base_url))
api.add_resource(medicos_registros,"{}/RegistrosMedicos".format(base_url))
api.add_resource(brindar_especialidades_paciente,"{}/BrindarEspecialidadesPaciente".format(base_url))
api.add_resource(usuario,"{}/Usuario".format(base_url))

if __name__ == '__main__':
    app.run(debug=True)