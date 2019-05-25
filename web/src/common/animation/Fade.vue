<template>
  <transition name="fade">
    <slot></slot>
  </transition>
</template>

<script>
    export default {
        name: "fade"
    }
</script>

<style scoped>
  .fade-enter-active, .fade-leave-active{
    transition: opacity .2s;
  }
  .fade-enter, .fade-leave-to{
    opacity: 0;
  }
</style>
