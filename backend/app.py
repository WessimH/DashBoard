from flask import Flask
from flask_restx import Api
from routes import ns
from mwrogue.esports_client import EsportsClient
app = Flask(__name__)
api = Api(app, version='1.0', title='LoL Esports API', description='API for retrieving LoL Esports data')

# Initialize EsportsClient (no init_app method)
client = EsportsClient("lol")

# Add the namespace to the API
api.add_namespace(ns, path='/api')

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
