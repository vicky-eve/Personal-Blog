from app import create_app, db
from  flask_migrate import Migrate, MigrateCommand

from app.models import User, Blog, Subscribe, Quote, Comment
from flask_script import Manager, Server

app = create_app('production')
app = create_app('tests')

manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,User = User, Blog = Blog, Subscribe = Subscribe, Quote = Quote, Comment = Comment)
    
if __name__ == '__main__':
    manager.run()