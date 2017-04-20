# coding:utf-8

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def manager_db(opetions):
    if opetions == "create":
        db.create_all(app=app)
    elif opetions == "drop":
        if prompt_bool(
                "Are you sure you want to lose all your data"):
            db.drop_all(app=app)
    else:
        print "无效参数"


if __name__ == '__main__':
    manager.run()
