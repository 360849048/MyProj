import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
// import Versions from '../components/Versions'
import Srctransfer from '../components/SrcTransfer'
// import Iomaker from '../components/IoMaker'
import SearchResult from '../components/SearchResult'

Vue.use(VueRouter);

// 改用vue-router懒加载，缩短首次主页加载时间
const Iomaker = resolve => require(['../components/IoMaker.vue'], resolve);
const Versions = resolve => require(['../components/Versions.vue'], resolve);

export default new VueRouter({
  // 三种模式介绍
  // Hash: 使用URL的hash值来作为路由。支持所有浏览器，url中会带有#。 (默认)
  // History: 以来HTML5 History API 和服务器配置。参考官网中HTML5 History模式。但是刷新后会返回404，这个需要后台支持
  // Abstract： 支持所有javascript运行模式。如果发现没有浏览器的API，路由会自动强制进入这个模式。
  mode: 'history',
  routes: [
    {path: '/home', component: Home},
    {path: '/versions', component: Versions},
    {path: '/srctransfer', component: Srctransfer},
    {path: '/makeio', component: Iomaker},
    {path: '/search', component: SearchResult},
    {path: '*', redirect: '/home'}
  ]
})
