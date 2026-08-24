from flask import Flask
from config import Config
from routes.submit import submit_bp
from routes.feedback import feedback_bp
from routes.meta import meta_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend requests
    try:
        from flask_cors import CORS
        CORS(app, resources={r"/api/*": {"origins": "*"}})
    except ImportError:
        pass

    # Register blueprints
    app.register_blueprint(submit_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(meta_bp, url_prefix='/api')

    @app.route('/api/health', methods=['GET'])
    def health():
        return {"status": "ok", "service": "Marketplace Risk Detector API"}, 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
