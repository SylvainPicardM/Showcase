<template>
  <div class="container">
    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <h1 class="display-4">Showcase</h1>
          <p class="lead">Choose a run in list below</p>
      </div>
    </div>
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
                  v-on:change="sortTables()"   
                  id="selectParam" class="form-control">
            <option disabled value="">Choose Score for sorting tables</option>
            <option v-for="score in get_scores_names" :key="score">
              {{ score }}
            </option>
          </select>
        </div>
      </div>
      <hr>
      <div v-if="exp_runs.length > 0">
        <!-- TABLES RESULTATS -->
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
</style>

<script>
import axios from 'axios';

export default {
  name: 'Showcase',
  data() {
    return {
      names: [],
      selected_exp: '',
      selected_score: '',
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
    sortTables(){
      if (this.selected_score != ''){
        this.exp_runs.sort(compareValues(this.selected_score))
      }
    }
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
  created() {
    this.getExpNames();
  },
  filters: {
    round(number) {
      return number.toPrecision(3)
    },
  },
};



// function for dynamic sorting
function compareValues(key, order='asc') {
  return function(a, b) {
    if(!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) {
      // property doesn't exist on either object
      return 0;
    }

    const varA = (typeof a[key] === 'string') ?
      a[key].toUpperCase() : a[key];
    const varB = (typeof b[key] === 'string') ?
      b[key].toUpperCase() : b[key];

    let comparison = 0;
    if (varA > varB) {
      comparison = 1;
    } else if (varA < varB) {
      comparison = -1;
    }
    return (
      (order == 'desc') ? (comparison * -1) : comparison
    );
  };
}
</script>
