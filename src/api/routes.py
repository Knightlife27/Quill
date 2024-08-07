from flask import Blueprint, jsonify, request
from .models import db, Dashboard, Chart
from .utils import APIException, execute_sql_query, apply_date_filter
from datetime import datetime, timedelta
import logging

api = Blueprint('api', __name__)

@api.route('/dashboard/<name>', methods=['GET'])
def get_dashboard(name):
    try:
        dashboard = Dashboard.query.filter_by(name=name).first()
        if not dashboard:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        charts = Chart.query.filter_by(dashboard_name=name).all()
        
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
