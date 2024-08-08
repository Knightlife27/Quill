from flask import jsonify, url_for
from supabase import create_client, Client
import os
from datetime import datetime, timedelta
import logging
from .models import Dashboard  # Assuming you have a models.py file with your ORM models
from sqlalchemy import func

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your project by following the <a href="https://start.4geeksacademy.com/starters/full-stack" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"

# Supabase client setup
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def execute_sql_query(sql_query):
    try:
        logging.info(f"Executing SQL query: {sql_query}")
        response = supabase.rpc('execute_sql', {'query': sql_query}).execute()
        
        if hasattr(response, 'data'):
            logging.info(f"SQL query executed successfully, response: {response.data[:5]}...")  # Log first 5 rows
            return [row['result'] for row in response.data]  # Extract 'result' from each row
        else:
            logging.error(f"Error executing SQL query: {response}")
            raise APIException(f"Error executing SQL query: No data returned")
    except Exception as e:
        logging.error(f"Exception in execute_sql_query: {str(e)}")
        raise APIException(f"Error executing SQL query: {str(e)}")

def apply_date_filter(sql_query, table_name, date_field, start_date, end_date):
    try:
        date_filter = f" WHERE {table_name}.{date_field} BETWEEN '{start_date}' AND '{end_date}'"
        
        if "WHERE" in sql_query.upper():
            filtered_query = sql_query.replace("WHERE", f"WHERE {table_name}.{date_field} BETWEEN '{start_date}' AND '{end_date}' AND", 1)
        else:
            filtered_query = sql_query + date_filter
        
        logging.info(f"Filtered SQL query: {filtered_query}")
        return filtered_query
    except Exception as e:
        logging.error(f"Exception in apply_date_filter: {str(e)}")
        raise APIException(f"Error applying date filter: {str(e)}")

def fetch_chart_data(chart, start_date, end_date):
    try:
        filtered_query = apply_date_filter(chart.sql_query, chart.date_field['table'], chart.date_field['field'], start_date, end_date)
        data = execute_sql_query(filtered_query)
        return data
    except Exception as e:
        logging.error(f"Error fetching chart data: {str(e)}")
        return []

def fetch_dashboard_by_name(name):
    """
    Fetch a dashboard by its name from the database.
    """
    try:
        dashboard = Dashboard.query.filter(func.lower(func.trim(Dashboard.name)) == func.lower(func.trim(name))).first()
        if not dashboard:
            logging.warning(f"Dashboard not found: {name}")
            return None
        logging.info(f"Dashboard found: {dashboard.name}")
        return dashboard
    except Exception as e:
        logging.error(f"Error fetching dashboard by name: {str(e)}")
        return None

def get_dashboard_data(name, start_date, end_date):
    dashboard = fetch_dashboard_by_name(name)
    if not dashboard:
        return jsonify({'error': 'Dashboard not found'}), 404
    charts_with_data = []
    for chart in dashboard.charts:  # Assuming Dashboard has a relationship with Chart
        chart_data = fetch_chart_data(chart, start_date, end_date)
        chart_dict = chart.serialize()
        chart_dict['data'] = chart_data
        charts_with_data.append(chart_dict)
    return jsonify({
        'dashboard': dashboard.serialize(),
        'charts': charts_with_data
    })