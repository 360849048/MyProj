<template>
  <div id="svgContainer" :class="[direction === 'left' ? 'left' : 'right']">
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
      <path v-if="direction === 'left'" d="M0 0 C0 100 50 100 50 200 50 300 0 300 0 400"></path>
      <path v-else d="M50 0 C50 100 0 100 0 200 0 300 50 300 50 400"></path>
    </svg>
    <i class="fa fa-3x" :class="[direction === 'left' ? 'fa-angle-left' : 'fa-angle-right']"></i>
  </div>
</template>

<script>
  export default {
    name: "swtitch-page",
    props: {
      direction: String,
    }
  }
</script>

<style lang="scss" scoped>
  #svgContainer {
    position: fixed;
    top: 50%;
    transform: translateY(-200px);
    width: 50px;
    height: 400px;
    opacity: 0;
    transition: opacity .3s;
    &:hover {
      opacity: 1;
    }
    svg {
      height: 100%;
      width: 100%;
      position: absolute;
      top: 0;
      left: 0;
      fill: rgba(200, 200, 200, .4);
    }
    i {
      position: absolute;
      top: 50%;
      left: 25%;
      transform: translateY(-24px);
    }
  }
  .left {
    left: 0;
    margin-left: -40px;
    &:hover {
      margin-left: 0;
    }
  }
  .right {
    right: 0;
    margin-right: -40px;
    &:hover {
      margin-right: 0;
    }
  }
</style>
