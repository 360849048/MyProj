import Vue from 'vue'
import App from './App.vue'
import router from './vueRouterConfig'
import store from './store'
import { Loading, Notification, InputNumber, Message, Pagination, Select, Option, Slider, Popover } from 'element-ui'

Vue.use(Loading);
Vue.prototype.$notify = Notification;
Vue.use(InputNumber);
Vue.prototype.$message = Message;
// 使用Pagination组件，会占用超级多的js容量(约100k)
Vue.use(Pagination);
Vue.use(Select);
Vue.use(Option);
Vue.use(Slider);
Vue.use(Popover);

new Vue({
  el: '#app',
  store,
  render: h => h(App),
  router
});
