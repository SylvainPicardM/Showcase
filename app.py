from flask import Flask, jsonify
from flask_cors import CORS
import json
from outfit import Wardrobe, Experiment, Feature, Output, Parameter, Score

# Config
with open('config.json') as f:
    config = json.load(f)

# App
app = Flask(__name__)
app.config.from_object(__name__)

# CORS
CORS(app, ressources={r'/*': {'origins': '*'}})

wardrobe = Wardrobe(db_path=config['DB_PATH'])

@app.route('/exp_names/', methods=['GET'])
def get_exp_names():
    data = {}
    query = Experiment.select(Experiment.id_experiment, Experiment.experiment_name)
    names = []
    for res in query.dicts():
        names.append(res['experiment_name'])
    data['names'] = list(set(names))
    return jsonify(data)

@app.route('/exp_details/<exp_name>', methods=['GET'])
def get_exp_details(exp_name):
    data = {}
    data['query_name'] = exp_name
    query = (Experiment.select(Experiment.id_experiment, Experiment.experiment_name)
                      .where(Experiment.experiment_name == exp_name))
    runs = []
    for res in query.dicts():
        run = {}
        run['experiment_name'] = res['experiment_name'] 
        run['id_experiment'] = res['id_experiment'] 
        query_param = Parameter.select().where(Parameter.experiment == run['id_experiment'])
        for res_param in query_param.dicts():
            print(res_param)
            run[res_param['parameter_name']] = res_param['parameter']
        runs.append(run)
    data['runs'] = runs
    return jsonify(data)




if __name__ == "__main_":
    app.run()
