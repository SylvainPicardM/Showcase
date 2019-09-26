<template>
  <div class="container">
    <ul>
        <li v-for="name in names"> {{ name }} </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Showcase',
  data() {
    return {
      names: [],
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/exp_names';
      axios.get(path).then((res) => {
        this.names = res.data.names;
      }).catch((error) => {
        console.log(error);
      });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
