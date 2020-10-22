from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView #,BaseModelView
from flask_admin.model import BaseModelView
from database.postsqldb.db import db
from database.postsqldb.models import LastappearedModel,MachineTypeModel,ExceptionTypeModel,ObjectTrajactoryModel

class MyModelView(ModelView):
    #column_formatters = dict(price=lambda v, c, m, p: m.price*2)

    column_display_pk=True
    create_modal = True
    edit_modal = True
    form_columns = ('lastappeared_id', 'exceptiontype')
    #column_editable_list = ('object_id', 'exceptiontype')
    column_list = ('lastappeared_id', 'exceptiontype')
    # def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
    #     #kwargs["list_columns"]=['object_id', 'exceptiontype']
    #     for k, v in kwargs.items():
    #         setattr(self, k, v)

    #     super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    # def is_accessible(self):
    #     # Logic
    #     return True
    #,list_columns=['object_id', 'exceptiontype']
def initialize_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(MachineTypeModel, db.session))
    admin.add_view(MyModelView(ExceptionTypeModel, db.session))
    admin.add_view(ModelView(LastappearedModel, db.session))
    admin.add_view(ModelView(ObjectTrajactoryModel, db.session))
    return admin