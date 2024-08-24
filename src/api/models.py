# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import JSON
# import uuid
# from . import db

# db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return f'<User {self.email}>'

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#         }

# class Dashboard(db.Model):
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String(255), unique=True, nullable=False)
#     date_filter = db.Column(JSON, nullable=False)

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'dateFilter': self.date_filter
#         }

# class Chart(db.Model):
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String, nullable=False)
#     dashboard_name = db.Column(db.String, db.ForeignKey('dashboard.name'), nullable=False)
#     chart_type = db.Column(db.String, nullable=False)
#     sql_query = db.Column(db.Text, nullable=False)
#     x_axis_field = db.Column(db.String, nullable=False)
#     y_axis_field = db.Column(db.String, nullable=False)
#     date_field = db.Column(JSON, nullable=False)

#     def serialize(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'dashboardName': self.dashboard_name,
#             'chartType': self.chart_type,
#             'sqlQuery': self.sql_query,
#             'xAxisField': self.x_axis_field,
#             'yAxisField': self.y_axis_field,
#             'dateField': self.date_field
#         }
    
#     # class KPIMetric(db.Model):
#     #     id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     #     dashboard_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('dashboard.id'), nullable=False)
#     #     metric_name = db.Column(db.String(255), nullable=False)
#     #     metric_value = db.Column(db.Float, nullable=False)
#     #     metric_unit = db.Column(db.String(50))

#     #     def serialize(self):
#     #         return {
#     #             'id': str(self.id),
#     #             'dashboard_id': str(self.dashboard_id),
#     #             'metric_name': self.metric_name,
#     #             'metric_value': self.metric_value,
#     #             'metric_unit': self.metric_unit
#     #         }

#     class KPIMetric(db.Model):
#         id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#         dashboard_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('dashboard.id'), nullable=False)
#         kpi_type = db.Column(db.String(50), nullable=False)  # Add this line
#         metric_name = db.Column(db.String(255), nullable=False)
#         metric_value = db.Column(db.Float, nullable=False)
#         metric_unit = db.Column(db.String(50))
#         date = db.Column(db.Date, nullable=False)

#         def serialize(self):
#             return {
#                 'id': str(self.id),
#                 'dashboard_id': str(self.dashboard_id),
#                 'kpi_type': self.kpi_type,
#                 'metric_name': self.metric_name,
#                 'metric_value': self.metric_value,
#                 'metric_unit': self.metric_unit,
#                 'date': self.date.isoformat()
#         }


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import uuid

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
        }

class Dashboard(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False)
    date_filter = db.Column(JSON, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'dateFilter': self.date_filter
        }

class Chart(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
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

# class KPIMetric(db.Model):
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     dashboard_id = db.Column(db.String(36), db.ForeignKey('dashboard.id'), nullable=False)
#     kpi_type = db.Column(db.String(50), nullable=False)
#     metric_name = db.Column(db.String(255), nullable=False)
#     metric_value = db.Column(db.Float, nullable=False)
#     metric_unit = db.Column(db.String(50))
#     date = db.Column(db.Date, nullable=False)

#     def serialize(self):
#         return {
#             'id': self.id,
#             'dashboard_id': self.dashboard_id,
#             'kpi_type': self.kpi_type,
#             'metric_name': self.metric_name,
#             'metric_value': self.metric_value,
#             'metric_unit': self.metric_unit,
#             'date': self.date.isoformat()
#         }

import uuid
from datetime import date

class KPIMetric(db.Model):
    __tablename__ = 'kpi_metrics'  # Make sure this matches your database table name
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dashboard_id = db.Column(db.String(36), db.ForeignKey('dashboard.id'), nullable=False)
    kpi_type = db.Column(db.String(50), nullable=False)
    metric_name = db.Column(db.String(255), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    metric_unit = db.Column(db.String(50))
    date = db.Column(db.Date, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'dashboard_id': self.dashboard_id,
            'kpi_type': self.kpi_type,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_unit': self.metric_unit,
            'date': self.date.isoformat() if isinstance(self.date, date) else self.date
        }