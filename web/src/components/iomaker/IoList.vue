<template>
    <div id="iolist">
      <div class="row">
        <!--  左侧IO类型选择导航 -->
        <div class="col-sm-2">
          <div class="nav flex-column nav-pills io-nav" id="v-pills-tab" role="tablist" aria-orientation="vertical">
            <a class="nav-link active" data-toggle="pill" href="#" role="tab" @click="ioType='di'">DI</a>
            <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='do'">DO</a>
            <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='ai'">AI</a>
            <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='ao'">AO</a>
            <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='ti'">TI</a>
            <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='to'">TO</a>
          </div>
        </div>
        <div class="col-sm-10">
          <!-- 上方页码标签 -->
          <ul class="nav nav-tabs">
            <li class="nav-item" v-for="eachPage in pages" @click="gotoPage(eachPage)">
              <a class="nav-link" :class="{'active': curPage === eachPage}" href="#">{{eachPage}}</a>
            </li>
          </ul>
          <!-- IO显示区 -->
          <div class="row" v-loading="loading">
            <div class="col-sm-6">
              <ul>
                <li v-for="(input, index) in ios" v-if="index < Math.ceil((curPageStartItem + curPageEndItem)/2)">
                  <div class="alert alert-primary" role="alert"
                       :data-index="index" :data-name="input"
                       draggable="true" @dragstart="dragIO">
                    {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                  </div>
                </li>
              </ul>
            </div>
            <div class="col-sm-6">
              <ul>
                <li v-for="(input, index) in ios" v-if="index >= Math.ceil((curPageStartItem + curPageEndItem)/2)">
                  <div class="alert alert-primary" role="alert"
                       :data-index="index" :data-name="input"
                       draggable="true" @dragstart="dragIO">
                    {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  /**
   * 数据处理逻辑:
   * 1.常量pageItemAmount规定一页最多显示的数据，
   * 2.通过ajax的get方式从后台按需获取当页所需要的数据，并非一次性全部得到所有数据。
   *  第一次ajax请求某类IO时数据量按pageItemAmount来（服务器允许请求数据超过实际服务器数据库容量），
   *  在服务器返回某类IO的数量，即更新了IoNum值以后，页码数才可以正确显示，后续此类IO的请求量也按实际数量来
   *
   */
  // 规定一页最多显示的数据
  const pageItemAmount = 32;

  export default {
    name: "io-list",
    data(){
      return {
        ioType: 'di',
        ioNum: pageItemAmount,       // 初始化足够大的值，确保第一次请求的数据足够显示
        ios: {},                     // 当前页面的IO序号(key)和对应的名称(value)
        curPage: 1,
        loading: true,
      }
    },
    computed: {
      /**
       * 根据服务器返回的正确ioNum计算得到实际应显示的页码
       * @return {Array}   例如[1,2,3,4]
       */
      pages: function(){
        let pageAmount = Math.ceil( this.ioNum / pageItemAmount );
        let pgs = [];
        for(let i=1; i<= pageAmount; i++){
          pgs.push(i);
        }
        return pgs
      },
      /**
       * 根据curPage值计算当前页面的起始IO序号
       * @return {number}
       */
      curPageStartItem: function(){
        return 1 + (this.curPage - 1) * pageItemAmount
      },
      /**
       * 根据curPage和ioNum值计算当前页面的最后一个IO序号
       * @return {number}
       */
      curPageEndItem: function(){
        return this.curPage * pageItemAmount < this.ioNum ? this.curPage * pageItemAmount : this.ioNum;
      }
    },
    methods: {
      /**
       * 点击某个页码后跳转到相应的IO显示
       * @param curPage
       * @return {number}
       */
      gotoPage(curPage){
        if (this.pages.indexOf(curPage) === -1){
          return -1;
        }
        // 不能在获取到this.ios之前改变当前页面，否则会导致页面切换时候闪屏
        // this.curPage = curPage;
        let curPageStartItem = 1 + (curPage - 1) * pageItemAmount;
        let curPageEndItem = curPage * pageItemAmount < this.ioNum ? curPage * pageItemAmount : this.ioNum;


        let _this = this;
        $.ajax({
          url: "/io",
          type: 'GET',
          dataType: 'json',
          beforeSend: function(){
            _this.loading = true;
          },
          complete: function(){
            _this.loading = false;
            _this.curPage = curPage;
          },
          data: {"type": _this.ioType, "start": curPageStartItem, 'end': curPageEndItem},
          success: function(data){
            _this.ioNum = data.amount;
            // json数据内部按key排序，可直接使用
            _this.ios = data.ios;
          },
          error: function(){
            console.log('Error!!!');
            _this.ioNum = 120;
            let temp = {};
            for(let i=curPageStartItem; i<=curPageEndItem; i++){
              temp[i] = i;
            }
            _this.ios = temp;
          }
        });
        return 0;
      },
      /**
       * 响应HTML5的dragstart事件，这个事件发送的数据可以在其他任意组件通过ondrop等事件接收
       * @param e
       */
      dragIO(e){
        // 通过拖拽的方式向ModuleConfig.vue传递io信息，格式例如："di--1--阀门1开"
        e.dataTransfer.setData('ioInfo', this.ioType + '--' + e.target.getAttribute('data-index') + '--' + e.target.getAttribute('data-name'));
      },
    },
    watch: {
      /**
       * 当左侧IO类型导航栏发生点击导致IO类型切换时，执行这个函数
       */
      ioType: {
        handler: function(cval, oval){
          // 切换不同io页面需要重置this.ioNum，确保获取到足够多的数据
          this.ioNum = pageItemAmount;
          this.gotoPage(1)
        },
        immediate: true
      }
    },
  }
</script>

<style scoped lang="scss">
  ul{
    list-style-type: none;
  }
  .io-nav{
    margin-top: 30px;
  }
  .nav.nav-tabs{
    margin: 10px;
    .nav-item{
      display: inline-block;
      width: 100px;
      text-align: center;
    }
  }
  .alert .badge-light{
    float: right;
  }
  .alert{
    /* Overwrite default bootstrap style */
    width: 80%;
    display: inline-block;
    padding: .15rem 1.25rem;
    margin-bottom: 0.25rem;
    user-select: none;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
  }
</style>
