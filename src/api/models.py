from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Dashboard(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    date_filter = db.Column(JSON, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'dateFilter': self.date_filter
        }

class Chart(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dashboard_name = db.Column(db.String, db.ForeignKey('dashboard.name'), nullable=False)
    chart_type = db.Column(db.String, nullable=False)
    sql_query = db.Column(db.Text, nullable=False)
    x_axis_field = db.Column(db.String, nullable=False)
    y_axis_field = db.Column(db.String, nullable=False)
    date_field = db.Column(JSON, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'dashboardName': self.dashboard_name,
            'chartType': self.chart_type,
            'sqlQuery': self.sql_query,
            'xAxisField': self.x_axis_field,
            'yAxisField': self.y_axis_field,
            'dateField': self.date_field
        }