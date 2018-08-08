import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import { Loading, Notification, Button, InputNumber } from 'element-ui'

Vue.use(Loading);
Vue.prototype.$notify = Notification;
Vue.use(Button);
Vue.use(InputNumber);

new Vue({
  el: '#app',
  render: h => h(App),
  router
});
