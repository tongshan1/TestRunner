import os
import warnings
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from werkzeug.contrib.fixers import ProxyFix


from src.app import create_app, db

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
app.wsgi_app = ProxyFix(app.wsgi_app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


def init():
    pass


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    manager.run()