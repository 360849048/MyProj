<template>
  <div id="app">
    <nav-view></nav-view>
    <keep-alive exclude="search-result">
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
import NavView from "./Nav"
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      ajaxMsg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    NavView
  }
}
</script>

<style>
  #app{
    font-family: Microsoft Yahei;
  }
</style>
