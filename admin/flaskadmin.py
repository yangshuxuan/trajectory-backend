from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database.postsqldb.db import db
from database.postsqldb.models import LastappearedModel,MachineTypeModel,ExceptionTypeModel,ObjectTrajactoryModel

def initialize_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(MachineTypeModel, db.session))
    admin.add_view(ModelView(ExceptionTypeModel, db.session))
    admin.add_view(ModelView(LastappearedModel, db.session))
    admin.add_view(ModelView(ObjectTrajactoryModel, db.session))
    return admin