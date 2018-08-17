import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import { Loading, Notification, Button, InputNumber, Message } from 'element-ui'

Vue.use(Loading);
Vue.prototype.$notify = Notification;
Vue.use(Button);
Vue.use(InputNumber);
Vue.prototype.$message = Message;

new Vue({
  el: '#app',
  render: h => h(App),
  router
});
