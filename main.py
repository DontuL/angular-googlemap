# main.py

from flask import Flask
from flask import send_file
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

# Strinfa di connessione al DB
app.config["MONGO_URI"] = "mongodb+srv://Tecno:Colibasi11@cluster0.8mdg9.mongodb.net/relab1.Mil4326WKT?retryWrites=true&w=majority"

mongo = PyMongo(app)
# Per rispondere alle chiamate cross origin
CORS(app)

# Annotation that allows the function to be hit at the specific URL.
@app.route("/")
# Generic Python functino that returns "Hello world!"
def index():
    return "Hello world!"
@app.route("/books")
# Generic Python functino that returns books.json
def books():
    return send_file('books.json')
# Questa route effettua una find() su tutto il DB (si limita ai primi 100 risultati)
@app.route('/addresses', methods=['GET'])
def get_all_addresses():
    mil4326WKT = mongo.db.Mil4326WKT
    output = []
    for s in mil4326WKT.find().limit(100):
        output.append(s['INDIRIZZO'] + s['CI_VETTORE'])
    return jsonify({'result': output})
@app.route('/ci_vettore/<foglio>', methods=['GET'])
def get_vettore(foglio):
    mil4326WKT = mongo.db.Mil4326WKT
    output = []
    query = {
        "FOGLIO" : foglio
    }
    for s in mil4326WKT.find(query):
        output.append({
            "INDIRIZZO":s['INDIRIZZO'],
            "WGS84_X":s["WGS84_X"],
            "WGS84_Y":s["WGS84_Y"],
            "CLASSE_ENE":s["CLASSE_ENE"],
            "EP_H_ND":s["EP_H_ND"],
            "FOGLIO":s["FOGLIO"],
            "CI_VETTORE":s['CI_VETTORE']
        }
        )
    return jsonify(output)
@app.route('/ci_vetttore/<sez>', methods=['GET'])
def get_vetttore(sez):
    mil4326WKT = mongo.db.Mil4326WKT
    output = []
    query = {
        "SEZ" : sez
    }
    for s in mil4326WKT.find(query):
        output.append({
            "INDIRIZZO":s['INDIRIZZO'],
            "CLASSE_ENE":s["CLASSE_ENE"],
            "EP_H_ND":s["EP_H_ND"],
            "SEZ":s['SEZ'],
        }
        )
    return jsonify(output)
# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
    # Runs the Flask application only if the main.py file is being run.
    app.run()

