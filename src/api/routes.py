from flask import Blueprint, jsonify, request
from .models import db, Dashboard, Chart
from .utils import APIException, execute_sql_query, apply_date_filter
from datetime import datetime, timedelta
from sqlalchemy import func, inspect
import logging


logging.basicConfig(level=logging.INFO)

api = Blueprint('api', __name__)

@api.route('/dashboard/<name>', methods=['GET'])
def get_dashboard(name):
    logging.info(f"Received request for dashboard: {name}")
    try:
        # Extract startDate and endDate from request arguments
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')

        # If start_date or end_date is not provided, use default date range
        if not start_date or not end_date:
            logging.warning("Start date or end date is missing, using default date range")
            dashboard = Dashboard.query.filter(func.lower(func.trim(Dashboard.name)) == func.lower(func.trim(name))).first()
            if not dashboard:
                logging.warning(f"Dashboard not found: {name}")
                return jsonify({'error': 'Dashboard not found'}), 404

            initial_date_range = dashboard.date_filter.get('initialDateRange', 'LAST_90_DAYS')
            start_date, end_date = get_date_range(initial_date_range)
        else:
            logging.info(f"Using date range: {start_date} to {end_date}")

        logging.info(f"Searching for dashboard by name: {name}")
        dashboard = Dashboard.query.filter(func.lower(func.trim(Dashboard.name)) == func.lower(func.trim(name))).first()
        
        if not dashboard:
            logging.warning(f"Dashboard not found: {name}")
            return jsonify({'error': 'Dashboard not found'}), 404
        
        logging.info(f"Dashboard found: {dashboard.name}")
        
        charts = Chart.query.filter_by(dashboard_name=dashboard.name).all()
        
        charts_with_data = []
        for chart in charts:
            try:
                logging.info(f"Fetching data for chart: {chart.name}")
                # Pass the extracted start_date and end_date to fetch_chart_data
                chart_data = fetch_chart_data(chart, start_date, end_date)
                chart_dict = chart.serialize()
                chart_dict['data'] = chart_data
                charts_with_data.append(chart_dict)
            except Exception as e:
                logging.error(f"Error fetching data for chart {chart.name}: {str(e)}")
                import traceback
                traceback.print_exc()
                charts_with_data.append(chart.serialize())  # Add chart without data
        
        logging.info(f"Successfully fetched data for dashboard: {dashboard.name}")
        return jsonify({
            'dashboard': dashboard.serialize(),
            'charts': charts_with_data
        })
    except Exception as e:
        logging.error(f"Error in get_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/chart/<id>', methods=['GET'])
def get_chart(id):
    logging.info(f"Fetching chart by ID: {id}")
    try:
        chart = Chart.query.get(id)
        if not chart:
            logging.warning(f"Chart not found: {id}")
            return jsonify({'error': 'Chart not found'}), 404
        
        start_date, end_date = get_date_range('LAST_90_DAYS')  # Default to last 90 days
        chart_data = fetch_chart_data(chart, start_date, end_date)
        chart_dict = chart.serialize()
        chart_dict['data'] = chart_data
        return jsonify(chart_dict)
    except Exception as e:
        logging.error(f"Error in get_chart: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/dashboards', methods=['GET'])
def list_all_dashboards():
    logging.info("Listing all dashboards")
    try:
        dashboards = Dashboard.query.all()
        return jsonify([{'id': d.id, 'name': d.name} for d in dashboards])
    except Exception as e:
        logging.error(f"Error in list_all_dashboards: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/db-test', methods=['GET'])
def test_db_connection():
    logging.info("Testing database connection")
    try:
        result = db.session.execute("SELECT 1").fetchone()
        if result[0] == 1:
            logging.info("Database connection successful")
            return jsonify({"message": "Database connection successful"})
        else:
            logging.error("Unexpected result from database")
            return jsonify({"error": "Unexpected result from database"}), 500
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Database connection failed: {str(e)}"}), 500

@api.route('/db-schema', methods=['GET'])
def get_db_schema():
    logging.info("Fetching database schema")
    try:
        inspector = inspect(db.engine)
        schemas = {}
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append(f"{column['name']} ({column['type']})")
            schemas[table_name] = columns
        return jsonify(schemas)
    except Exception as e:
        logging.error(f"Error getting database schema: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to get database schema: {str(e)}"}), 500

@api.route('/create-test-dashboard', methods=['POST'])
def create_test_dashboard():
    logging.info("Creating test dashboard")
    try:
        new_dashboard = Dashboard(
            name="Test Dashboard",
            date_filter={"initialDateRange": "LAST_90_DAYS"}
        )
        db.session.add(new_dashboard)
        db.session.commit()
        logging.info(f"Test dashboard created with ID: {new_dashboard.id}")
        return jsonify({"message": "Test dashboard created", "id": str(new_dashboard.id)}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating test dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to create test dashboard: {str(e)}"}), 500

@api.route('/test', methods=['GET'])
def test_route():
    logging.info("Test route accessed")
    return jsonify({"message": "Test route working"}), 200

@api.route('/raw-dashboards', methods=['GET'])
def get_raw_dashboards():
    logging.info("Fetching raw dashboards")
    try:
        result = db.session.execute("SELECT * FROM dashboard").fetchall()
        return jsonify([dict(row) for row in result])
    except Exception as e:
        logging.error(f"Error in get_raw_dashboards: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/create-chart', methods=['POST'])
def create_chart():
    logging.info("Creating new chart")
    try:
        data = request.get_json()
        new_chart = Chart(
            name=data['name'],
            dashboard_name=data['dashboard_name'],
            chart_type=data['chart_type'],
            sql_query=data['sql_query'],
            x_axis_field=data['x_axis_field'],
            y_axis_field=data['y_axis_field'],
            date_field=data['date_field']
        )
        db.session.add(new_chart)
        db.session.commit()
        logging.info(f"Chart created with ID: {new_chart.id}")
        return jsonify({"message": "Chart created", "id": str(new_chart.id)}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating chart: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to create chart: {str(e)}"}), 500

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

def fetch_chart_data(chart, start_date=None, end_date=None):
    try:
        date_field = chart.date_field
        table_name = date_field['table']
        field_name = date_field['field']
        
        logging.info(f"Fetching data for chart: {chart.name}")
        if start_date is None or end_date is None:
            logging.error("Start date or end date is None")
            return []  # Handle the case where dates are not provided
        
        logging.info(f"Date range: {start_date} to {end_date}")
        logging.info(f"SQL query before filter: {chart.sql_query}")
        
        # Apply the date filter to the SQL query
        filtered_query = apply_date_filter(chart.sql_query, table_name, field_name, start_date, end_date)
        logging.info(f"Filtered SQL query: {filtered_query}")
        
        # Execute the filtered SQL query
        data = execute_sql_query(filtered_query)
        logging.info(f"Raw data fetched: {data[:5]}...")  # Log first 5 rows for debugging
        
        if not data:
            logging.warning(f"No data returned for chart: {chart.name}")
            return []
        
        # Process the data for the chart
        processed_data = [
            {chart.x_axis_field: row.get(chart.x_axis_field), chart.y_axis_field: row.get(chart.y_axis_field)}
            for row in data if chart.x_axis_field in row and chart.y_axis_field in row
        ]
        logging.info(f"Processed data: {processed_data[:5]}...")  # Log first 5 rows for debugging
        
        return processed_data
    except Exception as e:
        logging.error(f"Error in fetch_chart_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return []  # Return an empty list instead of raising an exception

def apply_date_filter(sql_query, table_name, date_field, start_date, end_date):
    try:
        # Add WHERE clause for date filtering
        date_filter = f" WHERE {table_name}.{date_field} BETWEEN '{start_date}' AND '{end_date}'"
        
        # Check if the query already has a WHERE clause
        if "WHERE" in sql_query.upper():
            # If it does, add the date filter with AND
            filtered_query = sql_query.replace("WHERE", f"WHERE {table_name}.{date_field} BETWEEN '{start_date}' AND '{end_date}' AND", 1)
        else:
            # If it doesn't, add the date filter as a new WHERE clause
            filtered_query = sql_query + date_filter
        
        logging.info(f"Filtered SQL query: {filtered_query}")
        return filtered_query
    except Exception as e:
        logging.error(f"Exception in apply_date_filter: {str(e)}")
        raise APIException(f"Error applying date filter: {str(e)}")