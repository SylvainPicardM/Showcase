import Vue from 'vue';
import Router from 'vue-router';
import ShowCase from './components/Showcase.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: ShowCase,
    },
  ],
});
