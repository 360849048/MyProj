import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import { loading } from 'element-ui'

Vue.use(loading);

new Vue({
  el: '#app',
  render: h => h(App),
  router
});
