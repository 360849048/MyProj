<template>
  <div id="svgContainer" ref="svgContainer" @mouseup="handleDotMouseUp">
    <div class="info-wrapper" v-show="showInfo">
      <div class="title no-select">三次贝塞尔曲线测试</div>
      <div class="type-select">
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadio1" name="drawTypeRadio" class="custom-control-input" value=0 v-model="drawType">
          <label class="custom-control-label" for="customRadio1">方式1</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadio2" name="drawTypeRadio" class="custom-control-input" value=1 v-model="drawType">
          <label class="custom-control-label" for="customRadio2">方式2</label>
        </div>
      </div>
      <div class="c-adjust" v-show="drawType==='1'">
        <span class="demonstration">系数</span>
        <el-slider v-model="bezierC" :min=0 :max=100 :format-tooltip="formatTooltip"></el-slider>
      </div>
      <div class="ctrl-type" v-show="drawType==='1'">
        <div class="custom-control custom-radio">
          <input type="radio" id="customRadio3" name="ctrlDotCalcType" class="custom-control-input" value=0 v-model="ctrlType">
          <label class="custom-control-label" for="customRadio3">光滑曲线连接所有点</label>
        </div>
        <div class="custom-control custom-radio">
          <input type="radio" id="customRadio4" name="ctrlDotCalcType" class="custom-control-input" value=1 v-model="ctrlType">
          <label class="custom-control-label" for="customRadio4">S曲线连接相邻点</label>
        </div>
      </div>
      <div class="toggle-dotsdisp custom-control custom-checkbox">
        <input type="checkbox" class="custom-control-input" id="customCheck1" value=true v-model="showDots">
        <label class="custom-control-label" for="customCheck1">显示点</label>
      </div>
      <div class="tips">tips: 拖动红点以改变曲线</div>
      <div class="ctrl-widget" @click="showInfo=false">
        <i class="fa fa-angle-left fa-3x"></i>
      </div>
    </div>
    <div class="svg-wrapper" ref="svgWrapper">
      <svg xmlns="http://www.w3.org/2000/svg" version="1.1"  @click="handleSvgClick">
        <path :d="pathDesc" fill="transparent" stroke="black" stroke-width="5"></path>
        <template v-for="(dot, idx) in dots" v-if="showDots">
          <circle :cx="dot.x" :cy="dot.y" r="5" fill="red" :data-idx="idx"
            @mousedown="handleDotMouseDown"
            ></circle>
          <text :x="dot.x" :y="dot.y" fill="#666" transform="translate(5, 0)" class="no-select"
            :data-idx="idx"
            @click.stop="handleTextClick">
            P{{idx}}({{dot.x}}, {{dot.y}})
          </text>
        </template>
      </svg>
      <transition name="fade">
        <div class="input-container" ref="inputContainer" v-show="showInputs" @keyup.enter="handlePosChange">
          <p>分别输入x和y坐标</p>
          <div class="input-group">
            <input type="number" class="form-control inputX" v-model="inputX">
            <input type="number" class="form-control inputY" v-model="inputY">
            <button class="btn btn-outline-success" @click="handlePosChange">确定</button>
          </div>
        </div>
      </transition>
      <div class="ctrl-widget" v-show="!showInfo" @click="showInfo=true">
        <i class="fa fa-angle-right fa-3x"></i>
      </div>
    </div>
  </div>
</template>

<script>

  const calcBezierCtrlDot = function (prevDot, curDot, nextDot, c=0.5) {
    /**
     * 计算三次贝赛尔曲线的控制点a, b，使曲线光滑的连接所有的点（a，b两个控制点属于两条不同的三次贝塞尔曲线）。
     * 具体方法如下：
     *  将某一个点curDot与相邻两个点（prevDoo, nextDot）分别连接，构成两条线段，在这两条线段上，按系数c分别获取到一个点，
     *  默认c=0.5时，取到的是这两条线段的中点。
     *  连接这两个中点，得到一条线段。
     *  平移这条线段，并使得它的中点正好与curDot重合，此时线段的两端点a和b就是curDot前后的两个控制点
     */
    let tempDot1 = {x: (prevDot.x + curDot.x) * c, y: (prevDot.y + curDot.y) * c};
    let tempDot2 = {x: (curDot.x + nextDot.x) * c, y: (curDot.y + nextDot.y) * c};
    let tempDot3 = {x: (tempDot1.x + tempDot2.x) / 2, y: (tempDot1.y + tempDot2.y) / 2};
    let offsetX = curDot.x - tempDot3.x;
    let offsetY = curDot.y - tempDot3.y;
    let a = {x: (tempDot1.x + offsetX), y: (tempDot1.y + offsetY)};
    let b = {x: (tempDot2.x + offsetX), y: (tempDot2.y + offsetY)};
    return [a, b];
  };

  const calcBezierCtrlDot2 = function (prevDot, curDot, nextDot, c=0.5) {
    /**
     * 以S曲线的方式，计算三次贝塞尔曲线的控制点a，b（a，b两个控制点属于两条不同的三次贝塞尔曲线）。
     * 注意：这里S曲线针对垂直排布的点位
     */
    let a = {x: curDot.x, y: (prevDot.y - curDot.y) * c + curDot.y};
    let b = {x: curDot.x, y: (nextDot.y - curDot.y) * c + curDot.y};
    return [a, b];
  };

  export default {
    name: "bezier",
    data () {
      return {
        dots: [
          {y: 100, x: 200},
          {y: 200, x: 200},
          {y: 300, x: 200},
          {y: 400, x: 200},
          {y: 500, x: 200},
          {y: 600, x: 200},
          {y: 700, x: 200},
        ],
        curSelectedDot: 0,
        inputX: 0,
        inputY: 0,
        showInputs: false,
        showInfo: true,
        showDots: true,
        drawType: '0',
        ctrlType: '0',
        bezierC: 50
      }
    },
    computed: {
      pathDesc () {
        // Path路径描述，这里绘制三次贝塞尔曲线，格式：M10 10C20 20 30 30 40 40C50 50 60 60 70...
        let desc = '';
        if (this.drawType === '0') {
          // 将某些点作为控制点，直接生成三次贝塞尔曲线
          // 要求点的数量必须满足：3*三次贝塞尔C数量 + 1
          // 即this.dots数量必须是 4、7、10、...
          if (this.dots.length < 4 || this.dots.length % 3 !== 1) return;
          desc = `M${this.dots[0].x} ${this.dots[0].y}`;

          for (let i=0; i<(this.dots.length - 1) / 3; i++) {
            desc += `C${this.dots[i*3+1].x} ${this.dots[i*3+1].y} ${this.dots[i*3+2].x} ${this.dots[i*3+2].y} ${this.dots[i*3+3].x} ${this.dots[i*3+3].y}`
          }
        } else {
          // 将this.dots中的所有点用曲线连接起来，控制点由程序自动得到
          if (this.dots.length < 3) return;
          let prevDot, nextDot, curDot;
          let lastDotIdx = this.dots.length - 1;
          let offsetX, offsetY;
          let a, b;            // 控制点a和b
          let allDots = [];    // 包含起始点、两个控制点和结束点的所有点位集合。
          for (let i=0; i<=lastDotIdx; i++) {
            curDot = this.dots[i];
            if (i === 0) {
              offsetX = this.dots[0].x - this.dots[lastDotIdx].x;
              offsetY = this.dots[0].y - this.dots[lastDotIdx].y;
              prevDot = {x: this.dots[lastDotIdx - 1].x + offsetX, y: this.dots[lastDotIdx - 1].y + offsetY};
              nextDot = this.dots[1];

              allDots.push(this.dots[0]);
              if (this.ctrlType === '0') {
                [a, b] = calcBezierCtrlDot(prevDot, curDot, nextDot, this.bezierC/100);
              } else {
                [a, b] = calcBezierCtrlDot2(prevDot, curDot, nextDot, this.bezierC/100);
              }
              allDots.push(b);
            } else if(i === lastDotIdx) {
              offsetX = this.dots[lastDotIdx].x - this.dots[0].x;
              offsetY = this.dots[lastDotIdx].y - this.dots[0].y;
              prevDot = this.dots[lastDotIdx - 1];
              nextDot = {x: this.dots[1].x + offsetX, y: this.dots[1].y + offsetY};

              if (this.ctrlType === '0') {
                [a, b] = calcBezierCtrlDot(prevDot, curDot, nextDot, this.bezierC/100);
              } else {
                [a, b] = calcBezierCtrlDot2(prevDot, curDot, nextDot, this.bezierC/100);
              }
              allDots.push(a);
              allDots.push(this.dots[lastDotIdx]);
            } else {
              prevDot = this.dots[i - 1];
              nextDot = this.dots[i + 1];

              if (this.ctrlType === '0') {
                [a, b] = calcBezierCtrlDot(prevDot, curDot, nextDot, this.bezierC/100);
              } else {
                [a, b] = calcBezierCtrlDot2(prevDot, curDot, nextDot, this.bezierC/100);
              }
              allDots.push(a);
              allDots.push(curDot);
              allDots.push(b);
            }

          }

          desc = `M${allDots[0].x} ${allDots[0].y}`;
          for (let i=0; i<(allDots.length - 1) / 3; i++) {
            desc += `C${allDots[i*3+1].x} ${allDots[i*3+1].y} ${allDots[i*3+2].x} ${allDots[i*3+2].y} ${allDots[i*3+3].x} ${allDots[i*3+3].y}`
          }
        }
        return desc;
      }
    },
    methods: {
      handleDotMouseDown (e) {
        this.curSelectedDot = e.target.getAttribute('data-idx');
        this.$refs.svgContainer.addEventListener('mousemove', this.handleDotMouseMove);
      },
      handleDotMouseMove (e) {
        this.dots[this.curSelectedDot].x = e.pageX - this.$refs.svgWrapper.offsetLeft;
        this.dots[this.curSelectedDot].y = e.pageY - this.$refs.svgWrapper.offsetTop;
      },
      handleDotMouseUp (e) {
        this.$refs.svgContainer.removeEventListener('mousemove', this.handleDotMouseMove);
      },
      handleTextClick (e) {
        this.curSelectedDot = e.target.getAttribute('data-idx');
        this.inputX = this.dots[this.curSelectedDot].x;
        this.inputY = this.dots[this.curSelectedDot].y;
        this.$refs.inputContainer.style.left = this.inputX + 'px';
        this.$refs.inputContainer.style.top = this.inputY + 'px';
        this.showInputs = true;
      },
      handleSvgClick (e) {
        if (this.showInputs) this.showInputs = false;
      },
      handlePosChange () {
        this.dots[this.curSelectedDot].x = parseInt(this.inputX);
        this.dots[this.curSelectedDot].y = parseInt(this.inputY);
        this.showInputs = false;
      },
      formatTooltip(val) {
        return val / 100;
      }
    },
  }
</script>

<style scoped lang="scss">
  #svgContainer, svg {
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  #svgContainer {
    display: flex;
  }
  .info-wrapper {
    background-color: #eee;
    width: 200px;
    position: relative;
    margin: 0;
    .title {
      font-size: 20px;
    }
    .type-select {
      margin-top: 10px;
    }
    .tips {
      margin-top: 20px;
    }
    .ctrl-widget {
      position: absolute;
      top: 50%;
      right: 0;
      &:hover {
        cursor: pointer;
      }
    }
    .c-adjust {
      margin: 10px;
    }
  }
  .svg-wrapper {
    position: relative;
    flex: 1;
    .ctrl-widget {
      position: absolute;
      top: 50%;
      left: 0;
      &:hover {
        cursor: pointer;
      }
    }
  }
  .no-select {
    user-select: none;
    cursor: default;
  }
  .input-container {
    position: absolute;
    /*height: 100px;*/
    padding: 10px;
    z-index: 10;
    outline: 1px solid gray;
    box-shadow: 5px 5px 10px #ccc;
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
  .fade-enter-active, .fade-leave-active {
    transition: opacity .1s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>
