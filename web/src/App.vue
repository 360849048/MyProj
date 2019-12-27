<template>
  <div id="app">
    <nav-view></nav-view>
    <keep-alive exclude="search-result">
      <router-view></router-view>
    </keep-alive>
    <!--<i class="snowbox fa fa-android"></i>-->
  </div>
</template>

<script>
import NavView from "./nav/Nav"
import axios from 'axios'


const SNOW_NUM = 15;
const MAX_SPEED = 50;
const MIN_SPEED = 5;

export default {
  name: 'app',
  data () {
    return {
    }
  },
  components: {
    NavView
  },
  mounted () {
    function createSnow () {
      // 初始1个雪花随机位置和速度和大小
      let domSnow = document.createElement("i");
      domSnow.classList.add("snowbox", "fa", "fa-snowflake-o");
      document.body.appendChild(domSnow);
      let snowSpeed = MAX_SPEED * Math.random();
      snowSpeed = snowSpeed < MIN_SPEED ? MIN_SPEED : snowSpeed;
      let position = document.body.offsetWidth * Math.random();
      domSnow.style.left = position + 'px';
      domSnow.style.top = '0px';
      domSnow.style.fontSize = 2 * Math.random() + 'rem';

      function moveSnow () {
        // 垂直掉落
        let curTop = parseInt(domSnow.offsetTop);
        if (curTop >= document.body.offsetHeight + 20) {
          document.body.removeChild(domSnow);
          createSnow();
          return;
        }
        domSnow.style.top = curTop + snowSpeed + 'px';
        // 左右摇摆
        let curLeft = parseInt(domSnow.offsetLeft);
        if (curLeft >= document.body.offsetWidth + 20 || curLeft <= -20) {
          document.body.removeChild(domSnow);
          createSnow();
          return;
        }
        if (Math.random() > 0.5) {
          domSnow.style.left = curLeft + Math.ceil(snowSpeed / 10 * Math.random()) + 'px';
        } else {
          domSnow.style.left = curLeft - Math.ceil(snowSpeed / 10 * Math.random()) + 'px';
        }
        // 随着高度改变透明度
        domSnow.style.opacity = 1 - curTop / document.body.offsetHeight;
          window.setTimeout(moveSnow, 500);
      }
      moveSnow();
    }
    for (let i=0; i<SNOW_NUM; i++) {
      createSnow();
    }
  }
}
</script>

<style>
  #app{
    font-family: Microsoft Yahei;
  }
  .snowbox {
    position: fixed;
    color: #eee;
    transition: linear .5s;
  }
</style>
