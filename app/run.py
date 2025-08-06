from flask import Flask
from dotenv import load_dotenv
import os

#  Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")  # ✅ Load secret key from .env

#  Register the blueprint
from routes.detect import detect_bp
app.register_blueprint(detect_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)