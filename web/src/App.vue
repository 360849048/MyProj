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

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
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
