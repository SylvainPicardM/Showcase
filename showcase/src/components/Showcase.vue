<template>
  <div class="container">
    <!-- HEADER -->
    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <h1 class="display-4">Showcase</h1>
      </div>
    </div>
    <!-- SELECT RUN AND SORT -->
    <div class="form-row">
      <div class="col">
        <select v-model="selected_exp" 
                v-on:change="getExpDetails()" 
                id="selectRun" class="form-control">
            <option v-for="name in names" v-bind:key="name">
                {{ name }}
            </option>
        </select>
      </div>
      <div class="col">
        <select v-model="selected_score"
                id="selectParam" class="form-control">
          <option disabled value="">Choose Score for sorting tables</option>
          <option v-for="score in get_scores_names" :key="score">
            {{ score }}
          </option>
        </select>
      </div>
      <div class="col">
        <select v-model="selected_param"
                id="selectParam" class="form-control">
          <option disabled value="">Choose Parameter for sorting tables</option>
          <option v-for="param in get_params_names" :key="param">
            {{ param }}
          </option>
        </select>
      </div>
    </div>
    <hr>
    <div v-if="exp_runs.length > 0">
      <!-- TABLES RESULTATS -->
      <div id="result-tables">
        <table class="table table-sm table-hover">
            <thead class="thead-dark">
                <tr>
                    <th>RUN_ID</th>
                    <th scope="col" v-for="param in get_params_names">{{ param }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="run in exp_runs">
                    <td>{{ run.id_experiment }}</td>
                    <td v-for="p in run.parameters">{{ p }}</td>
                </tr>
            </tbody>
        </table>
        <table class="table table-sm table-hover">
            <thead class="thead-dark">
                <tr>
                    <th>RUN_ID</th>
                    <th scope="col" v-for="param in get_scores_names">{{ param }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="run in exp_runs">
                    <td>{{ run.id_experiment }}</td>
                    <td v-for="s in run.scores">{{ s | round }}</td>
                </tr>
            </tbody>
        </table>
      </div>
      <hr>
      <div id="graphs">
        <div class="form-row">
          <div class="col-4">
            <select v-model="selected_param"
                    id="selectParam" class="form-control">
              <option disabled value="">Choose Parameter to generate graphs</option>
              <option v-for="param in get_params_names" :key="param">
                {{ param }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.table{
  margin-bottom: 50px;
}
.table tr{
  cursor: pointer;
}
.table th, td{
  text-align: center;
}
div{
  margin-bottom: 10px;
}
</style>

<script>
import axios from 'axios';
var _ = require('lodash');

export default {
  name: 'Showcase',
  data() {
    return {
      names: [],
      selected_exp: '',
      selected_score: '',
      selected_param: '',
      exp_runs: [],
      select_run: '',
    };
  },
  methods: {
    getExpNames() {
      const path = 'http://localhost:5000/exp_names';
      axios.get(path).then((res) => {
        this.names = res.data.names;
      }).catch((error) => {
        console.log(error);
      });
    },
    getExpDetails() {
      if (this.selected_exp != ''){
        const path = `http://localhost:5000/exp_details/${this.selected_exp}`;
        axios.get(path).then((res) => {
          this.exp_runs = res.data.runs;
        }).catch((error) => {
          console.log(error);
        });
      }
    },
  },
  computed: {
    get_params_names() {
      if (this.exp_runs.length == 0){
        return '';
      } else{
        return Object.keys(this.exp_runs[0].parameters);
      }
    },
    get_scores_names() {
      if (this.exp_runs.length == 0){
        return '';
      } else{
        return Object.keys(this.exp_runs[0].scores);
      }
    },
  },
  watch: {
    selected_score(newScore, oldScore) {
      if (newScore != ''){
        this.selected_param = '';
        this.exp_runs = _.orderBy(this.exp_runs, function(a) { return a.scores[newScore] }, ['desc']);
      }
    },
    selected_param(newParam, oldParam) {
      if (newParam != ''){
        this.selected_score = '';
        this.exp_runs = _.orderBy(this.exp_runs, function(a) { return a.parameters[newParam] }, ['desc']);
      }
    },
  },
  filters: {
    round(number) {
      return number.toPrecision(3)
    },
  },
  created() {
    this.getExpNames();
  },
};
</script>
