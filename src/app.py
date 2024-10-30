"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client
from api.models import db, Dashboard, Chart
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from api.utils import APIException, generate_sitemap
from flask_jwt_extended import JWTManager
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Handle proxy headers from Render
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    raise ValueError("DATABASE_URL environment variable is not set")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("FLASK_APP_KEY", "sample key")
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 24 * 60 * 60
jwt = JWTManager(app)

# Initialize the database
db.init_app(app)
MIGRATE = Migrate(app, db, compare_type=True)

# CORS Configuration
cors = CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://datadesk-io-47ep.onrender.com",
            "http://localhost:3000",
            "http://localhost:3001"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 600  # Cache preflight requests for 10 minutes
    }
})

# Error Handling for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

# Setup admin and commands
setup_admin(app)
setup_commands(app)

# Environment setup
ENV = os.getenv("FLASK_ENV", "development")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public')

# Error handlers
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    logger.error(f"API Exception: {str(error)}")
    return jsonify(error.to_dict()), error.status_code

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Internal Server Error: {str(error)}")
    return jsonify({"error": "Internal Server Error"}), 500

# Sitemap
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# Serve static files
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response

# Supabase configuration
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Route to fetch chart data from Supabase
@app.route('/api/charts', methods=['GET'])
def get_charts():
    try:
        response = supabase.table('Chart').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        logger.error(f"Error fetching charts: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Route to fetch all dashboards
@app.route('/api/dashboards', methods=['GET'])
def list_all_dashboards():
    try:
        dashboards = Dashboard.query.all()
        return jsonify([{'id': d.id, 'name': d.name} for d in dashboards])
    except Exception as e:
        logger.error(f"Error fetching dashboards: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Route to fetch a specific dashboard
@app.route('/api/dashboards/<int:dashboard_id>', methods=['GET'])
def get_dashboard(dashboard_id):
    try:
        dashboard = Dashboard.query.get(dashboard_id)
        if dashboard:
            return jsonify({
                'id': dashboard.id,
                'name': dashboard.name,
                'charts': [{'id': c.id, 'name': c.name} for c in dashboard.charts]
            })
        else:
            return jsonify({'error': 'Dashboard not found'}), 404
    except Exception as e:
        logger.error(f"Error fetching dashboard {dashboard_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=ENV == "development")