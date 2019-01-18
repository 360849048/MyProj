<template>
  <div id="svgContainer" ref="svgContainer">
    <h1 class="no-select">拖动红点改变曲线</h1>
    <div class="svg-wrapper" ref="svgWrapper">
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
        <path :d="'M'+x0+' '+y0+'Q'+x1+' '+y1+' '+x2+' '+ y2" fill="transparent" stroke="black" stroke-width="5"></path>
        <circle :cx="x0" :cy="y0" r="5" fill="red" id="dot0"
                @mousedown="handleMousedown"
                @mouseup="handleMouseup"></circle>
        <text :x="x0" :y="y0" fill="#666" transform="translate(5,0)" class="no-select">P0({{x0}}, {{y0}})</text>
        <circle :cx="x1" :cy="y1" r="5" fill="red" id="dot1"
                @mousedown="handleMousedown"
                @mouseup="handleMouseup"></circle>
        <text :x="x1" :y="y1" fill="#666" transform="translate(5,0)" class="no-select">P1({{x1}}, {{y1}})</text>
        <circle :cx="x2" :cy="y2" r="5" fill="red" id="dot2"
                @mousedown="handleMousedown"
                @mouseup="handleMouseup"></circle>
        <text :x="x2" :y="y2" fill="#666" transform="translate(5,0)" class="no-select">P2({{x2}}, {{y2}})</text>
      </svg>
    </div>
  </div>
</template>

<script>
  export default {
    name: "bezier",
    data () {
      return {
        x0: 100,
        y0: 200,
        x1: 150,
        y1: 400,
        x2: 200,
        y2: 600,
        curSelectedDot: 0
      }
    },
    methods: {
      handleMousedown (e) {
        this.$refs.svgContainer.onmousemove = this.handleMousemove;

        if (e.target.id === 'dot0') {
          this.curSelectedDot = 0;
        }

        if (e.target.id === 'dot1') {
          this.curSelectedDot = 1;
        }

        if (e.target.id === 'dot2') {
          this.curSelectedDot = 2;
        }
      },
      handleMouseup (e) {
        this.$refs.svgContainer.onmousemove = null;
      },
      handleMousemove (e) {
        if (this.curSelectedDot === 0){
          this.x0 = e.pageX;
          this.y0 = e.pageY - this.$refs.svgWrapper.offsetTop;
        } else if (this.curSelectedDot === 1) {
          this.x1 = e.pageX;
          this.y1 = e.pageY - this.$refs.svgWrapper.offsetTop;
        } else if (this.curSelectedDot === 2) {
          this.x2 = e.pageX;
          this.y2 = e.pageY - this.$refs.svgWrapper.offsetTop;
        }
      }
    }
  }
</script>

<style scoped>
  #svgContainer:host {
    overflow: hidden;
    border: 1px red solid;
  }
  #svgContainer, .svg-wrapper, svg {
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  .svg-wrapper {
    /*border: 1px solid gray;*/
  }
  .no-select {
    user-select: none;
  }
</style>
