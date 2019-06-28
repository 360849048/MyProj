<template>
    <div id="iolist">
      <!--  左侧IO类型选择导航 -->
      <div class="io-type">
        <div class="nav flex-column nav-pills io-nav" id="v-pills-tab" role="tablist" aria-orientation="vertical">
          <a class="nav-link active" data-toggle="pill" href="#" role="tab" @click="ioType='DI'">DI</a>
          <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='DO'">DO</a>
          <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='AI'">AI</a>
          <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='AO'">AO</a>
          <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='TI'">TI</a>
          <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='TO'">TO</a>
        </div>
      </div>
      <div class="io-area">
        <!-- 上方页码标签 -->
        <ul class="nav nav-tabs">
          <li class="nav-item" v-for="eachPage in pages" @click="goto(eachPage)">
            <a class="nav-link" :class="{'active': curPage === eachPage}" href="##">{{eachPage}}</a>
          </li>
        </ul>
        <!-- IO显示区 -->
        <div class="disp-area" v-loading="loading">
          <div class="column column-1">
            <ul>
              <li v-for="(input, index) in ios" v-if="index <= Math.floor((curPageStartItem + curPageEndItem)/2)">
                <div class="alert" role="alert"
                     :class="[checkUsed(index) ? 'alert-secondary' : 'alert-primary']"
                     :data-index="index" :data-name="input"
                     draggable="true" @dragstart="dragIO"
                     @dblclick="dblClickIO">
                  {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                </div>
              </li>
            </ul>
          </div>
          <div class="column column-2">
            <ul>
              <li v-for="(input, index) in ios" v-if="index > Math.floor((curPageStartItem + curPageEndItem)/2)">
                <div class="alert alert-primary" role="alert"
                     :class="[checkUsed(index) ? 'alert-secondary' : 'alert-primary']"
                     :data-index="index" :data-name="input"
                     draggable="true" @dragstart="dragIO"
                     @dblclick="dblClickIO">
                  {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

  // 规定一页最多显示的数据
  const PAGE_ITEM_AMOUNT = 32;

  export default {
    name: "io-list",
    props: {
      allIO: Object,
      loading: Boolean,
      usedIO: Object
    },
    data(){
      return {
        ioType: 'DI',
        ios: {},                     // 当前页面的IO序号(key)和对应的名称(value)
        curPage: 1,
      }
    },
    computed: {
      pages: function(){
        if (this.loading) {
          return [1];
        }
        let pageAmount = Math.ceil( this.allIO[this.ioType].length / PAGE_ITEM_AMOUNT );
        let pgs = [];
        for(let i=1; i<= pageAmount; i++){
          pgs.push(i);
        }
        return pgs
      },
      curPageStartItem: function(){
        /**
         * 根据curPage值计算当前页面的起始IO序号
         * @return {number}
         */
        return 1 + (this.curPage - 1) * PAGE_ITEM_AMOUNT
      },
      curPageEndItem: function(){
        /**
         * 根据curPage和ioNum值计算当前页面的最后一个IO序号
         * @return {number}
         */
        let ioAmount = this.allIO[this.ioType].length;
        return this.curPage * PAGE_ITEM_AMOUNT < ioAmount ? this.curPage * PAGE_ITEM_AMOUNT : ioAmount;
      }
    },
    methods: {
      dragIO(e){
        /**
         * 响应HTML5的dragstart事件，这个事件发送的数据可以在其他任意组件通过ondrop等事件接收
         * @param e
         */
        // 通过拖拽的方式向ModuleConfig.vue传递io信息，格式例如："di--1"
        let ioIdx = e.target.getAttribute('data-index');
        if (this.checkUsed(ioIdx)) {
          e.preventDefault();
        } else {
          e.dataTransfer.setData('ioInfo', this.ioType + '--' + ioIdx);
        }
      },
      checkUsed(ioIdx){
        return this.usedIO[this.ioType].indexOf(parseInt(ioIdx)) !== -1;
      },
      dblClickIO(e){
        /**
         * 触发newioappend事件，向父组件发送当前发生鼠标双击的且未占用的IO。
         */
        // 格式例如："DI--1" （与上面的drag事件传递数据格式一致）
        let ioIdx = e.target.getAttribute('data-index');
        if(this.checkUsed(ioIdx)){
          return;
        }
        this.$emit('newioappend',  this.ioType + '--' + ioIdx);
      },
      goto (page) {
        if (this.loading || this.pages.indexOf(page) === -1) {
          return false;
        }
        this.curPage = page;

        let ioAmount = this.allIO[this.ioType].length;
        let curPageStartItem = 1 + (page - 1) * PAGE_ITEM_AMOUNT;
        let curPageEndItem = page * PAGE_ITEM_AMOUNT < ioAmount ? page * PAGE_ITEM_AMOUNT : ioAmount;

        let _ios = {};
        for (let i=curPageStartItem; i<=curPageEndItem; i++) {
          _ios[i] = this.allIO[this.ioType][i-1];
        }
        this.ios = _ios;
        return true;
      }
    },
    watch: {
      ioType: {
        /**
         * 当左侧IO类型导航栏发生点击导致IO类型切换时，执行这个函数
         */
        handler: function(){
          this.goto(1);
        }
      },
      loading: {
        handler: function (cv, ov) {
          if (ov && !cv) {
            this.goto(1);
          }
        }
      }
    },
  }
</script>

<style scoped lang="scss">
  ul{
    list-style-type: none;
  }
  .alert{
    /* Overwrite default bootstrap style */
    width: 100%;
    display: inline-block;
    padding: .15rem .6rem;
    margin-bottom: 0.25rem;
    user-select: none;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
  }
  #iolist {
    height: 100%;
    overflow: auto;
    display: flex;
    &::-webkit-scrollbar{
      width: 6px;
      height: 6px;
    }
    &::-webkit-scrollbar-thumb{
      border-radius: 10px;
      -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
      background: #818080;
    }
    .io-type {
      margin-top: 30px;
      max-width: 20%;
    }
    .io-area {
      width: 80%;
      .nav.nav-tabs{
        margin: 15px;
        .nav-item{
          display: inline-block;
          width: 20%;
          text-align: center;
        }
      }
      .disp-area {
        display: flex;
        .column {
          padding-left: .8rem;
        }
      }
      @media screen and (min-width: 992px) {
        .disp-area {
          .column {
            width: 50%;
          }
        }
      }
      @media screen and (max-width: 992px) {
        .disp-area {
          flex-wrap: wrap;
          .column {
            width: 100%;
          }
        }
      }
    }
  }
</style>
