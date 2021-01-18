import datetime
from .models_instance import exSql
from werkzeug.security import generate_password_hash,check_password_hash

db = exSql.db

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    identificacion = db.Column(db.BigInteger, unique = True)
    username = db.Column(db.String(40), unique = True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(94))
    direccion = db.Column(db.String(50))
    tipo = db.Column(db.String(20))
    servicios_medicos = db.Column(db.ARRAY(db.String(90)))
    fecha_nacimiento = db.Column(db.Date)
    especiliades_pacientes = db.relationship("especialidades_medico_paciente",backref='user')
    change_first_password = db.Column(db.Boolean,default=False)
    telefono = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime, default = datetime.datetime.now)
    
    def __init__(self,data): #se llama al iniciar
        self.username           = data['username']
        self.email              = data['email']
        self.fecha_nacimiento   = data['fecha_nacimiento']
        self.direccion          = data['direccion']
        self.identificacion     = data['identificacion']
        self.servicios_medicos  = data['servicios_medicos']
        self.telefono           = data['telefono']
        self.tipo               = data['tipo']
        self.password           = self.__create_password(data['password'])


    def __create_password(self,password): #funcion personalizada
        return generate_password_hash(password)

    def verify_password(self,password): #funcion personalizada
        return check_password_hash(self.password,password) #compara la passwords hasheada con la password en texto plano que pasa por argumento

class especialidades_medico_paciente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    medico = db.Column(db.Integer, db.ForeignKey(Usuarios.id))#medico
    paciente = db.Column(db.String(80))
    especialidades = db.Column(db.ARRAY(db.String(80)))
    usuario_medico = db.relationship('Usuarios', foreign_keys='especialidades_medico_paciente.medico') #para mostrarar el objeto medio en la lista de especialidades

    def __init__(self,medico,paciente,especialidades): #se llama al iniciar
        self.medico = medico
        self.paciente = paciente
        self.especialidades = especialidades