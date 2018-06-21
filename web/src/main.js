import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'

new Vue({
  el: '#app',
  render: h => h(App),
  router
})
