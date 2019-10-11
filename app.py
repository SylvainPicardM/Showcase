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
        run = {
            'parameters': {},
            'scores': {}
        }
        run['experiment_name'] = res['experiment_name'] 
        run['id_experiment'] = res['id_experiment'] 

        # Get parameters
        query_param = Parameter.select().where(Parameter.experiment == run['id_experiment'])
        for res_param in query_param.dicts():
            run['parameters'][res_param['parameter_name']] = res_param['parameter']

        # Get scores
        query_score = Score.select().where(Score.experiment == run['id_experiment'])
        for res_score in query_score.dicts():
            run['scores'][res_score['type_score']] = res_score['score']

        runs.append(run)
    data['runs'] = runs
    return jsonify(data)


@app.route('/delete_exp/<exp_id>', methods=['GET'])
def delete_run(exp_id):
    data = {"id": exp_id}
    n = Experiment.delete().where(Experiment.id_experiment == exp_id).execute()
    return jsonify(data)


if __name__ == "__main_":
    app.run()
