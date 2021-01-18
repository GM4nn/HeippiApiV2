from flask import request,Blueprint
from flask_restful import Resource, Api, marshal_with,marshal
from app.serializers import usuario_serializer,list_serializer,user_current_serializer,medicos_registros_serializer,registros_de_medicos_from_hospital
from app.models import Usuarios,especialidades_medico_paciente
from app.forms import CreateUserForm,especialidades_Medico_paciente
from .models_instance import exSql
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
import wtforms_json
import json
wtforms_json.init()

db = exSql.db

def validate_auth(data,ref_password_update = False):
    if not data.is_json:
        return {"mensaje": "Falta un json en la solicitud"}, 400
    identificacion = data.json.get('identificacion', None)
    password = data.json.get('password', None)
    if not identificacion:
        return {"mensaje": "Falta el parametro de identificacion"}, 400
    if not password:
        return {"mensaje": "Falta el parametro de password"}, 400
    username_current  = db.session.query(Usuarios).filter_by(identificacion = identificacion).first()
    if username_current is not None and username_current.verify_password(password):
        if username_current.tipo == "Medico" and username_current.change_first_password == 0 and not ref_password_update:
            return {"mensaje": "Debes cambiar tu contraseña"}, 400
        else:
            #user_current = dict(marshal(username_current,user_current_serializer)) #json de la entidad username
            user_current = username_current
            return user_current,200
    return {"mensaje": "identificacion o contraseñas invalidas"}, 401

def register_user(get_data):
    create_form = CreateUserForm.from_json(get_data)
    if create_form.validate():
        user =  user = Usuarios(create_form.data)
        db.session.add(user) #preparar la transaccion
        db.session.commit() # aqui nos aseguramos de que se escriba en la bd si ahy error hara un rolback
        return {'status':200,'mensaje':'Usuario creado correctamente'}
    else:
        return {'mensaje':'Error al enviar la informacion','errors':create_form.errors}

class sistema(Resource):
    decorators = [jwt_required]
    def get(self):
        return {"usuario":get_jwt_identity(),"mensaje":"este usuario esta logueado y en el sistema"}

class actualizar_password(Resource):
    def post(self):
        validate_user = validate_auth(request,True)
        if(validate_user[1] == 200):
            user = validate_user[0]
            new_password = request.json.get("new_password",None)
            if not new_password:
                return {'mensaje':"falta el parametro nueva contraseña"}
            hash_password = exSql.genera_hash(new_password)
            user.password = hash_password
            user.change_first_password = True
            db.session.add(user) #preparar la transaccion
            db.session.commit() # aqui nos aseguramos de que se escriba en la bd si ahy error hara un rolback
            return {'status':200,'mensaje':'Contraseña reestablecida correctamente'}
        return validate_auth(request)

class autentificacion(Resource):
    def post(self):
        if validate_auth(request)[1] == 200: #status_code
            user_current = dict(marshal(validate_auth(request)[0],user_current_serializer)) #json de la entidad username
            access_token = create_access_token(identity=user_current)
            return {"token":access_token}, 200
        return validate_auth(request)

class usuarios(Resource):
    def get(self):
        per_page = 2
        page = request.args.get('page',default = 1,type = int)
        usuarios = db.session.query(Usuarios).order_by(-Usuarios.id).paginate(page,per_page,False)
        return marshal(usuarios,list_serializer(usuario_serializer))
    def post(self):
        if(request.get_json()["tipo"] != "Medico"):
            return register_user(request.get_json())
        return {'mensaje':'No tienes permitido registrar medicos'} , 401

class medicos_registros(Resource):
    decorators = [jwt_required]
    #usuario tipo hospital puede ver todas las especialidades aplicadas de medicos a pacientes
    def get(self):
        if get_jwt_identity()['tipo'] == "Hospital":
            per_page = 2
            page = request.args.get('page',default = 1,type = int)
            esp_mec_pac = db.session.query(especialidades_medico_paciente).order_by(-especialidades_medico_paciente.id).paginate(page,per_page,False)
            return marshal(esp_mec_pac,list_serializer(registros_de_medicos_from_hospital))
        else:
            return {'mensaje':'Credenciales invalidas','errors':"Credenciales"}
    #Registrar un usuario de tipo medico siendo hospital
    def post(self):
        if(get_jwt_identity()['tipo'] == "Hospital" and request.get_json()["tipo"] == "Medico"):
            return register_user(request.get_json())
        else:
            return {'mensaje':'Credenciales invalidas','errors':"Credenciales"}

class brindar_especialidades_paciente(Resource):
    decorators = [jwt_required]
    def get(self):
        if(get_jwt_identity()['tipo'] == "Medico"):
            per_page = 2
            page = request.args.get('page',default = 1,type = int)
            #registros del medico que esta logueado
            esp_mec_pac = db.session.query(especialidades_medico_paciente).filter_by(medico = get_jwt_identity()['id']).order_by(-especialidades_medico_paciente.id).paginate(page,per_page,False)
            return marshal(esp_mec_pac,list_serializer(medicos_registros_serializer))
        else:
            return  {'mensaje':'Credenciales invalidas','errores':"Credenciales"}
    def post(self):
        if(get_jwt_identity()['tipo'] == "Medico"):
            #registrar una espeicalidad del paciente
            if request.method == "POST": 
                create_form = especialidades_Medico_paciente.from_json(request.get_json())
                if create_form.validate():
                    especialidades = especialidades_medico_paciente(
                            get_jwt_identity()['id'],
                            create_form.paciente.data,
                            create_form.especialidades.data
                    )
                    db.session.add(especialidades) #preparar la transaccion
                    db.session.commit() # aqui nos aseguramos de que se escriba en la bd si ahy error hara un rolback
                    return {'status':200,'mensaje':'aplicado la especialidades correctamente'},200
                else:
                    return {'mensaje':'Error al enviar la informacion','errors':create_form.errors},400
        else:
            return  {'mensaje':'Credenciales invalidas','errores':"Credenciales"}


class usuario(Resource):
    @jwt_required
    def get(self):
        user = Usuarios.query.filter_by(id=get_jwt_identity()['id']).first_or_404()
        return marshal(user,usuario_serializer)