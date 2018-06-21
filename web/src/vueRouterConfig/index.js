import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import Versions from '../components/Versions'
import Srctransfer from '../components/SrcTransfer'
import Srcmaker from  '../components/SrcMaker'

Vue.use(VueRouter);

export default new VueRouter({
    routes: [
        {path: '/home', component: Home},
        {path: '/versions', component: Versions},
        {path: '/srctransfer', component: Srctransfer},
        {path: '/srcmaker', component: Srcmaker},
        {path: '*', redirect: '/home'}
    ]
})