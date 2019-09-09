import Vue from 'vue'
import VueRouter from 'vue-router'
import Srctransfer from '../page/select/SrcTransfer'
import SearchResult from '../page/search/SearchResult'
import Bezier from '../page/bezier/Bezier'
import Log from '../page/Log/Log'


Vue.use(VueRouter);

// 改用vue-router懒加载，缩短首次主页加载时间
const Iomaker = () => import('../page/iomaker/IoMaker.vue');
const Versions = () => import('../page/versions/Versions.vue');
const Home = () => import('../page/home/Home.vue');

const router = new VueRouter({
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
    {path: '/bezier', component: Bezier},
    {path: '/log', component: Log},
    {path: '*', redirect: '/home'}
  ]
});

export default router
