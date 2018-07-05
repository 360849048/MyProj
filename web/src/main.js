import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import { Loading } from 'element-ui'

Vue.use(Loading);

new Vue({
  el: '#app',
  render: h => h(App),
  router
});
