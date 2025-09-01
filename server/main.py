from flask import Flask
from flask_cors import CORS
from routes import bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
