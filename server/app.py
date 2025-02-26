from flask import Flask, jsonify, request
from config import FLASK_SECRET_KEY
from metrics import metrics_blueprint, REQUEST_COUNT
from auth import auth_blueprint
from search import search_blueprint
from gemini import ai_blueprint
from user import user_blueprint
from chat import chat_blueprint
from flask_cors import CORS
from middleware import auth_handler, error_handler

app = Flask(__name__)  # Initialize Flask application instance
app.secret_key = FLASK_SECRET_KEY  # Set the Flask secret key for session management

# Register blueprints for API routes
app.register_blueprint(metrics_blueprint)
app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
app.register_blueprint(search_blueprint, url_prefix="/api/v1/search")
app.register_blueprint(ai_blueprint, url_prefix="/api/v1/ai")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/user")
app.register_blueprint(chat_blueprint, url_prefix="/api/v1/chat")

# Register middleware functions for authentication and error handling
app.before_request(auth_handler)
app.register_error_handler(Exception, error_handler)

# Enable CORS for all routes under /api/*
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://mivro.org",
                "https://*.mivro.org",
                "http://localhost:3000",
            ],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    },
)


@app.teardown_request
def increment_requests(response):
    if response is not None:
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            http_status=response.status_code,
        ).inc()
    return response


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)  # Run the app on localhost:5000 in debug mode
