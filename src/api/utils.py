from flask import jsonify, url_for
from supabase import create_client, Client
import os
from datetime import datetime, timedelta

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
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
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
        response = supabase.rpc('execute_sql', {'query': sql_query}).execute()
        return response.data
    except Exception as e:
        raise APIException(f"Error executing SQL query: {str(e)}")

def apply_date_filter(sql_query, date_field, start_date, end_date):
    if not date_field or not start_date or not end_date:
        return sql_query
    
    date_condition = f"WHERE {date_field} BETWEEN '{start_date}' AND '{end_date}'"
    
    if 'WHERE' in sql_query:
        sql_query = sql_query.replace('WHERE', f'{date_condition} AND')
    elif 'GROUP BY' in sql_query:
        parts = sql_query.split('GROUP BY')
        sql_query = f"{parts[0]} {date_condition} GROUP BY {parts[1]}"
    else:
        sql_query += f" {date_condition}"
    
    return sql_query