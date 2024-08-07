from flask import Blueprint, jsonify, request
from .models import db, Dashboard, Chart
from .utils import APIException, execute_sql_query, apply_date_filter
from datetime import datetime, timedelta
from sqlalchemy import func
import logging

api = Blueprint('api', __name__)

@api.route('/dashboard/<name>', methods=['GET'])
def get_dashboard(name):
    try:
        print(f"Searching for dashboard: {name}")
        dashboard = Dashboard.query.filter(func.lower(func.trim(Dashboard.name)) == func.lower(func.trim(name))).first()
        if not dashboard:
            print(f"Dashboard not found: {name}")
            # Let's print all dashboards to see what's in the database
            all_dashboards = Dashboard.query.all()
            print(f"All dashboards: {[d.name for d in all_dashboards]}")
            return jsonify({'error': 'Dashboard not found'}), 404
        
        print(f"Dashboard found: {dashboard.name}")
        
        charts = Chart.query.filter_by(dashboard_name=dashboard.name).all()
        
        initial_date_range = dashboard.date_filter['initialDateRange']
        start_date, end_date = get_date_range(initial_date_range)
        
        for chart in charts:
            chart_data = fetch_chart_data(chart, start_date, end_date)
            chart.data = chart_data
        
        return jsonify({
            'dashboard': dashboard.serialize(),
            'charts': [chart.serialize() for chart in charts]
        })
    except Exception as e:
        logging.error(f"Error in get_dashboard: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/dashboard/id/<id>', methods=['GET'])
def get_dashboard_by_id(id):
    try:
        dashboard = Dashboard.query.get(id)
        if not dashboard:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        charts = Chart.query.filter_by(dashboard_name=dashboard.name).all()
        
        initial_date_range = dashboard.date_filter['initialDateRange']
        start_date, end_date = get_date_range(initial_date_range)
        
        for chart in charts:
            chart_data = fetch_chart_data(chart, start_date, end_date)
            chart.data = chart_data
        
        return jsonify({
            'dashboard': dashboard.serialize(),
            'charts': [chart.serialize() for chart in charts]
        })
    except Exception as e:
        logging.error(f"Error in get_dashboard_by_id: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/chart/<id>', methods=['GET'])
def get_chart(id):
    try:
        chart = Chart.query.get(id)
        if not chart:
            return jsonify({'error': 'Chart not found'}), 404
        
        start_date, end_date = get_date_range('LAST_90_DAYS')  # Default to last 90 days
        chart_data = fetch_chart_data(chart, start_date, end_date)
        chart_dict = chart.serialize()
        chart_dict['data'] = chart_data
        return jsonify(chart_dict)
    except Exception as e:
        logging.error(f"Error in get_chart: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def get_date_range(range_type):
    today = datetime.now().date()
    if range_type == 'LAST_90_DAYS':
        return today - timedelta(days=90), today
    elif range_type == 'LAST_60_DAYS':
        return today - timedelta(days=60), today
    elif range_type == 'LAST_30_DAYS':
        return today - timedelta(days=30), today
    elif range_type == 'CURRENT_MONTH':
        return today.replace(day=1), today
    else:
        return today - timedelta(days=90), today  # Default to last 90 days

def fetch_chart_data(chart, start_date, end_date):
    date_field = chart.date_field
    table_name = date_field['table']
    field_name = date_field['field']
    
    filtered_query = apply_date_filter(chart.sql_query, table_name, field_name, start_date, end_date)
    data = execute_sql_query(filtered_query)
    
    processed_data = [
        {chart.x_axis_field: row[chart.x_axis_field], chart.y_axis_field: row[chart.y_axis_field]}
        for row in data
    ]
    
    return processed_data