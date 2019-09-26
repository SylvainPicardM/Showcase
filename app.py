from flask import Flask, jsonify
from flask_cors import CORS
import json
from outfit import Wardrobe, Experiment

# Config
with open('config.json') as f:
    config = json.load(f)

# App
app = Flask(__name__)
app.config.from_object(__name__)

# CORS
CORS(app, ressources={r'/*': {'origins': '*'}})

wardrobe = Wardrobe(db_path=config['DB_PATH'])

@app.route('/exp_names', methods=['GET'])
def index():
    data = {}
    query = Experiment.select(Experiment.id_experiment, Experiment.experiment_name)
    names = {}
    for res in query.dicts():
        names[res['id_experiment']] = res['experiment_name']
    data['names'] = names
    return jsonify(data)

if __name__ == "__main_":
    app.run()
