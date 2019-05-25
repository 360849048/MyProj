<template>
  <div id="funcMenu">
    <div class="main-wrapper">
      <div class="title" :title="name" :class="{'text-danger': value===0, 'text-success': value!==0}">{{name}}</div>
      <div class="value" ref="value" @click="toggleMenu">{{list[value]}}</div>
      <div class="arrow" :class="{'rotate': showMenu}" ref="arrow" @click="toggleMenu">
        <i class="fa fa-angle-left fa-x"></i>
      </div>
    </div>
    <Fade>
      <div class="drop-menu" v-show="showMenu && list.length" ref="menu">
        <div class="popper-arrow" ref="popperArrow"></div>
        <div class="item-wrapper"  v-for='(item, idx) in list' :key="idx">
          <div class="item" :class="{'selected': idx===value}" @click=choseItem(idx)>{{item}}</div>
        </div>
      </div>
    </Fade>
  </div>
</template>

<script>
  import Fade from '@/common/animation/Fade'

  export default {
    name: "func-menu",
    props: {
      name: String,
      list: Array,
    },
    components: {
      Fade
    },
    data () {
      return {
        showMenu: false,
        value: 0,
      }
    },
    methods: {
      toggleMenu () {
        if (!this.showMenu){
          this.$refs.popperArrow.style.left = this.$refs.arrow.offsetLeft - this.$refs.value.offsetLeft + 24  + 'px';
        }
        this.showMenu = !this.showMenu;
      },
      choseItem (idx) {
        this.value = idx;
        this.showMenu = !this.showMenu;
        this.$emit('itemchange', this.value);
      },
      hideMenu (e) {
        let dom = e.target;
        while (dom !== null) {
          if (dom === this.$refs.menu || dom === this.$refs.value || dom === this.$refs.arrow) {
            return;
          }
          dom = dom.parentElement;
        }
        this.showMenu = false;
      }
    },
    activated () {
      document.addEventListener('click', this.hideMenu);
    },
    deactivated () {
      document.removeEventListener('click', this.hideMenu);
    }
  }
</script>

<style scoped lang="scss">
  #funcMenu {
    position: relative;
    .drop-menu {
      position: absolute;
      left: 6rem;
      margin-left: -15px;
      font-size: 25px;
      background: #fff;
      border: 1px solid #666;
      box-shadow: 1px 1px 8px 0 #666;
      border-radius: 2px;
      z-index: 10;
      user-select: none;
      cursor: default;
      .popper-arrow {
        position: absolute;
        top: 0;
        margin-top: -10px;
        width: 10px;
        height: 10px;
        overflow: hidden;
        &::after {
          content: '';
          position: absolute;
          top: 60%;
          left: 0;
          width: 100%;
          height: 100%;
          display: inline-block;
          background-color: #fff;
          border: 1px solid #666;
          transform: rotate(45deg);
          box-shadow: 2px 2px 8px 0 #666;
        }
      }
      .item {
        padding: 0 40px 0 20px;
        color: #666;
        &:hover {
          background-color: #eee;
        }
      }
      .selected {
        background-color: #eee;
        color: black;
      }
    }
  }
  .main-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    line-height: 25px;
    font-size: 25px;
    padding: 0 5px;
    .title {
      width: 6rem;
      font-size: 20px;
      /*outline: red 1px dotted;*/
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
    }
    .value {
      cursor: pointer;
      /*outline: red 1px dotted;*/
      max-width: 60%;
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
    }
    .arrow {
      transform: rotate(-90deg);
      cursor: pointer;
      /*outline: red 1px dotted;*/
      padding: 8px;
      margin-left: 10px;
      transition: transform .2s ease;
    }
  }
  .rotate {
    transform: rotate(90deg) !important;
  }
</style>
