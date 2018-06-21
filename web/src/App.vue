<template>
  <div id="app">
    <nav-view></nav-view>
    <router-view></router-view>
  </div>
</template>

<script>
import NavView from "./components/Nav"

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

<style lang="scss">

</style>
