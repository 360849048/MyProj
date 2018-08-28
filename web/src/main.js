import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import { Loading, Notification, InputNumber, Message, Pagination } from 'element-ui'

Vue.use(Loading);
Vue.prototype.$notify = Notification;
Vue.use(InputNumber);
Vue.prototype.$message = Message;
// 使用Pagination组件，会占用超级多的js容量(约100k)
Vue.use(Pagination);

new Vue({
  el: '#app',
  render: h => h(App),
  router
});
