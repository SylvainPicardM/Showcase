<template>
  <div class="container">
    <h1>Showcase</h1>
      <div class="form-group">
        <label for="selectRun">Choisir run</label> 
        <select v-model="selected_exp" 
                v-on:change="getExpDetails()" 
                id="selectRun" class="form-control">
            <option v-for="name in names" v-bind:key="name">
                {{ name }}
            </option>
        </select>
      </div>
      <hr>
      <div v-if="exp_runs.length > 0">
        <table class="table table-sm">
            <thead>
                <tr>
                    <th scope="col" v-for="param in get_params_names">{{ param }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="run in exp_runs">
                    <td v-for="p in run.parameters">{{ p }}</td>
                </tr>
            </tbody>
        </table>
        <table class="table table-sm">
            <thead>
                <tr>
                    <th scope="col" v-for="param in get_scores_names">{{ param }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="run in exp_runs">
                    <td v-for="s in run.scores">{{ s }}</td>
                </tr>
            </tbody>
        </table>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Showcase',
  data() {
    return {
      names: [],
      selected_exp: '',
      exp_runs: [],
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
      const path = `http://localhost:5000/exp_details/${this.selected_exp}`;
      axios.get(path).then((res) => {
        this.exp_runs = res.data.runs;
      }).catch((error) => {
        console.log(error);
      });
    },
  },
  computed: {
    get_params_names() {
      return Object.keys(this.exp_runs[0].parameters);
    },
    get_scores_names() {
      return Object.keys(this.exp_runs[0].scores);
    },
  },
  created() {
    this.getExpNames();
  },
};
</script>
