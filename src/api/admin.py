import os
from flask_admin import Admin
from .models import db, User, Dashboard, Chart
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    class ModelViewExtended(ModelView):
        column_display_pk = True 
        def __init__(self, model, session, **kwargs):
            super(ModelViewExtended, self).__init__(model, session, **kwargs)
            
            self.column_list = tuple(model.__table__.columns.keys())
    
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Dashboard, db.session))
    admin.add_view(ModelViewExtended(Chart, db.session))
