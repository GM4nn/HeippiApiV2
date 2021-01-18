from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import *
from app_serve import app
from app.models_instance import exSql

migrate = Migrate(app, exSql.db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()