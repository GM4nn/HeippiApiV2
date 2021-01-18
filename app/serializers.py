from flask_restful import fields

user_current_serializer = {
    'id':fields.Integer,
    'change_first_password':  fields.Boolean,
    'tipo': fields.String,
}

usuario_serializer = {
    'identificacion':fields.Integer,
    'username':fields.String,
    'email':fields.String,
    'direccion':fields.String,
    'tipo': fields.String,
    'servicios_medicos':fields.List(fields.String),
    'fecha_nacimiento': fields.String,
    'change_first_password':  fields.Boolean,
    'telefono': fields.Integer,
    'created_date':fields.DateTime(dt_format='rfc822')
}


registros_de_medicos_from_hospital = {
    'id':fields.Integer,
    'usuario_medico':fields.Nested(usuario_serializer),
    'paciente':fields.String,
    'especialidades':fields.List(fields.String)
}


medicos_registros_serializer = {
    'id':fields.Integer,
    'paciente':fields.String,
    'especialidades':fields.List(fields.String)
}

def list_serializer(serializer_alone):
    list_serializer = {
        "page":fields.Integer,
        "per_page":fields.Integer,
        "items": fields.List(fields.Nested(serializer_alone))
    }
    return list_serializer