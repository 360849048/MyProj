<template>
  <div id="svgContainer" ref="svgContainer">
    <h1 class="no-select">拖动红点改变曲线</h1>
    <div class="svg-wrapper" ref="svgWrapper">
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1" @click="handleSvgClick">
        <path :d="'M'+x0+' '+y0+'Q'+x1+' '+y1+' '+x2+' '+ y2" fill="transparent" stroke="black" stroke-width="5"></path>
        <circle :cx="x0" :cy="y0" r="5" fill="red" id="dot0"
                @mousedown="handleMousedown"
                @mouseup="handleMouseup"></circle>
        <text :x="x0" :y="y0" fill="#666" transform="translate(5,0)" class="no-select" @click.stop="handleTextClick(0)">P0({{x0}}, {{y0}})</text>
        <circle :cx="x1" :cy="y1" r="5" fill="red" id="dot1"
                @mousedown="handleMousedown"
                @mouseup="handleMouseup"></circle>
        <text :x="x1" :y="y1" fill="#666" transform="translate(5,0)" class="no-select" @click.stop="handleTextClick(1)">P1({{x1}}, {{y1}})</text>
        <circle :cx="x2" :cy="y2" r="5" fill="red" id="dot2"
                @mousedown="handleMousedown"
                @mouseup="handleMouseup"></circle>
        <text :x="x2" :y="y2" fill="#666" transform="translate(5,0)" class="no-select" @click.stop="handleTextClick(2)">P2({{x2}}, {{y2}})</text>
      </svg>
      <div class="input-container" ref="inputContainer">
        <p>分别输入x和y坐标</p>
        <div class="input-group">
          <input type="number" class="form-control inputX" v-model="inputX">
          <input type="number" class="form-control inputY" v-model="inputY">
          <button class="btn btn-outline-success" @click="handleBtnClick">确定</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: "bezier",
    data () {
      return {
        x0: 300,
        y0: 200,
        x1: 350,
        y1: 400,
        x2: 400,
        y2: 600,
        curSelectedDot: 0,
        inputX: 0,
        inputY: 0
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
      },
      handleTextClick (point) {
        if (point === 0) {
          this.curSelectedDot = 0;
          this.$refs.inputContainer.style.left = this.x0 + 'px';
          this.$refs.inputContainer.style.top = this.y0 + 'px';
          this.inputX = this.x0;
          this.inputY = this.y0;
        } else if (point === 1) {
          this.curSelectedDot = 1;
          this.$refs.inputContainer.style.left = this.x1 + 'px';
          this.$refs.inputContainer.style.top = this.y1 + 'px';
          this.inputX = this.x1;
          this.inputY = this.y1;
        } else if (point === 2) {
          this.curSelectedDot = 2;
          this.$refs.inputContainer.style.left = this.x2 + 'px';
          this.$refs.inputContainer.style.top = this.y2 + 'px';
          this.inputX = this.x2;
          this.inputY = this.y2;
        }
        this.$refs.inputContainer.style.display = 'block';
      },
      handleSvgClick () {
        this.$refs.inputContainer.style.display = 'none';
      },
      handleBtnClick () {
        if (this.curSelectedDot === 0) {
          this.x0 = this.inputX;
          this.y0 = this.inputY;
        } else if (this.curSelectedDot === 1) {
          this.x1 = this.inputX;
          this.y1 = this.inputY;
        } else if (this.curSelectedDot === 2) {
          this.x2 = this.inputX;
          this.y2 = this.inputY;
        }
        this.$refs.inputContainer.style.display = 'none';
      }
    }
  }
</script>

<style scoped lang="scss">
  #svgContainer, .svg-wrapper, svg {
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  .svg-wrapper {
    position: relative;
  }
  .no-select {
    user-select: none;
    cursor: default;
  }
  .input-container {
    position: absolute;
    left: 0;
    top: 0;
    height: 100px;
    padding: 10px;
    z-index: 10;
    outline: 1px solid gray;
    box-shadow: 5px 5px 10px #ccc;
    display: none;
    background-color: #fff;
    .input-group {
      display: flex;
      justify-content: center;
      align-items: center;
      input {
        display: inline-block;
        width: 60px;
        margin-right: 5px;
        &::-webkit-outer-spin-button,
        &::-webkit-inner-spin-button{
          -webkit-appearance: none !important;
          margin: 0;
        }
      }
    }
  }
</style>
