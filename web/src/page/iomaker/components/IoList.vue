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
              <a class="nav-link" :class="{'active': curPage === eachPage}" href="##">{{eachPage}}</a>
            </li>
          </ul>
          <!-- IO显示区 -->
          <div class="row" v-loading="loading">
            <div class="col-sm-6">
              <ul>
                <li v-for="(input, index) in ios" v-if="index < Math.ceil((curPageStartItem + curPageEndItem)/2)">
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
            <div class="col-sm-6">
              <ul>
                <li v-for="(input, index) in ios" v-if="index >= Math.ceil((curPageStartItem + curPageEndItem)/2)">
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
    </div>
</template>

<script>
  /**
   * 数据处理逻辑:
   * 1.常量pageItemAmount规定一页最多显示的数据，
   * 2.通过ajax的get方式从后台按需获取当页所需要的数据，并非一次性全部得到所有数据。
   *  第一次ajax请求某类IO时数据量按pageItemAmount来（服务器允许请求数据超过实际服务器数据库容量），
   *  在服务器返回某类IO的数量，即更新了IoNum值以后，页码数才可以正确显示，后续此类IO的请求量也按实际数量来
   * 3.根据父组件传递过来的模块IO选择信息，将已选择的IO点，CSS样式区别于未选中的IO点。
   *
   */
  // 规定一页最多显示的数据
  const pageItemAmount = 32;

  export default {
      name: "io-list",
    props: ['boardModules1', 'boardModules2', 'boardModules3', 'boardModulesIOs1', 'boardModulesIOs2', 'boardModulesIOs3',
      'type', 'e73Safety', 'moldSlider', 'func1ToProgO1', 'func2ToProgO2'],
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
      pages: function(){
        /**
         * 根据服务器返回的正确ioNum计算得到实际应显示的页码
         * @return {Array}   例如[1,2,3,4]
         */
        let pageAmount = Math.ceil( this.ioNum / pageItemAmount );
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
        return 1 + (this.curPage - 1) * pageItemAmount
      },
      curPageEndItem: function(){
        /**
         * 根据curPage和ioNum值计算当前页面的最后一个IO序号
         * @return {number}
         */
        return this.curPage * pageItemAmount < this.ioNum ? this.curPage * pageItemAmount : this.ioNum;
      }
    },
    methods: {
      gotoPage(curPage){
        /**
         * 点击某个页码后跳转到相应的IO显示
         * @param curPage
         * @return {number}
         */
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
            console.log('AJAX请求失败，无法获取IO列表');
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
      dragIO(e){
        /**
         * 响应HTML5的dragstart事件，这个事件发送的数据可以在其他任意组件通过ondrop等事件接收
         * @param e
         */
        // 通过拖拽的方式向ModuleConfig.vue传递io信息，格式例如："di--1--阀门1开"
        e.dataTransfer.setData('ioInfo', this.ioType + '--' + e.target.getAttribute('data-index') + '--' + e.target.getAttribute('data-name'));
      },
      checkUsed(ioIdx){
        /**
         * 检查某个IO是否已经被选中到Module中，或被某些特殊功能占用
         *  该函数调用频率很高，比较耗费性能，里面不要写太复杂
         * @param ioIdx 某个IO的序号(字符串格式)，这里结合变量ioType，可以定位到具体某个IO点
         */
        for(let i=0; i<=this.boardModulesIOs1.length; i++) {
          for (let key in this.boardModulesIOs1[i]) {
            if (key.slice(0, 2).toUpperCase() === this.ioType.toUpperCase()) {
              if (this.boardModulesIOs1[i][key] === ioIdx) {
                return true;
              }
            }
          }
        }
        for(let i=0; i<=this.boardModulesIOs2.length; i++) {
          for (let key in this.boardModulesIOs2[i]) {
            if (key.slice(0, 2).toUpperCase() === this.ioType.toUpperCase()) {
              if (this.boardModulesIOs2[i][key] === ioIdx) {
                return true;
              }
            }
          }
        }
        for(let i=0; i<=this.boardModulesIOs3.length; i++) {
          for (let key in this.boardModulesIOs3[i]) {
            if (key.slice(0, 2).toUpperCase() === this.ioType.toUpperCase()) {
              if (this.boardModulesIOs3[i][key] === ioIdx) {
                return true;
              }
            }
          }
        }
        if(this.e73Safety && this.type !== 'VE2'){
          if(this.ioType.toUpperCase() === 'DI'){
            if(ioIdx === '110' || ioIdx === '111'){
              return true;
            }
          }
        }
        if(this.moldSlider){
          if(this.ioType.toUpperCase() === 'DI'){
            if(ioIdx === '73'){
              return true;
            }
          }
        }
        if(this.func1ToProgO1){
          if(this.ioType.toUpperCase() === 'DO'){
            if(ioIdx === '73'){
              return true;
            }
          }
        }
        if(this.func2ToProgO2){
          if(this.ioType.toUpperCase() === 'DO'){
            if(ioIdx === '74'){
              return true;
            }
          }
        }
        return false;
      },
      dblClickIO(e){
        /**
         * 触发newioappend事件，向父组件发送当前发生鼠标双击的且未占用的IO。
         */
        // 格式例如："di--1--阀门1开" （与上面的drag事件传递数据格式一致）
        let ioIdx = e.target.getAttribute('data-index');
        let ioName = e.target.getAttribute('data-name');
        if(this.checkUsed(ioIdx)){
          return;
        }
        this.$emit('newioappend',  this.ioType + '--' + ioIdx + '--' + ioName);
      }
    },
    watch: {
      ioType: {
        /**
         * 当左侧IO类型导航栏发生点击导致IO类型切换时，执行这个函数
         */
        handler: function(cval, oval){
          // 切换不同io页面需要重置this.ioNum，确保获取到足够多的数据
          // 但是不要轻易修改this.ioNum，否则会导致页面闪烁
          if(this.ioNum < pageItemAmount){
            this.ioNum = pageItemAmount;
          }
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
    margin: 15px;
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
    padding: 15px;
    &::-webkit-scrollbar{
      width: 6px;
      height: 6px;
    }
    &::-webkit-scrollbar-thumb{
      border-radius: 10px;
      -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
      background: #818080;
    }
  }
</style>
