<template>
  <div class="container">
    <h1>Showcase</h1>
      <div class="form-group">
        <label for="selectRun">Choisir run</label> 
        <select v-model="selected_exp" v-on:change="getExpDetails()" id="selectRun" class="form-control">
            <option v-for="name in names" v-bind:key="name">
                {{ name }}
            </option>
        </select>
      </div>
      <div>
        <p>{{ exp_details }}</p>
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
      exp_details: ''
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
      const path = 'http://localhost:5000/exp_details/' + this.selected_exp;
      axios.get(path).then(res => {
        this.exp_details = res.data;
      }).catch(error => {
        console.log(error);
      });
    },
  },
  created() {
    this.getExpNames();
  },
};
</script>
