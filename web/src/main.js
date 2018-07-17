import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import { Loading, Notification, Button } from 'element-ui'

Vue.use(Loading);
Vue.use(Button);
Vue.prototype.$notify = Notification;

new Vue({
  el: '#app',
  render: h => h(App),
  router
});
