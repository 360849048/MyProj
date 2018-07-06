<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- 左侧导航 -->
          <div class="col-sm-1">
            <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
              <a class="nav-link active" data-toggle="pill" href="#" role="tab" @click="ioType='di'">DI</a>
              <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='do'">DO</a>
              <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='ai'">AI</a>
              <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='ao'">AO</a>
              <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='ti'">TI</a>
              <a class="nav-link"  data-toggle="pill" href="#" role="tab" @click="ioType='to'">TO</a>
            </div>
          </div>
          <div class="col-sm-7">
            <!-- 上方导航 -->
            <ul class="nav nav-tabs">
              <li class="nav-item" v-for="eachPage in pages" @click="gotoPage(eachPage)">
                <a class="nav-link" :class="{'active': curPage === eachPage}" href="#">{{eachPage}}</a>
              </li>
            </ul>
            <!-- IO显示区 -->
            <div class="row" v-loading="loading">
              <div class="col-sm">
                <ul>
                  <li v-for="(input, index) in ios" v-if="index < Math.ceil((curPageStartItem + curPageEndItem)/2)">
                    <div class="alert alert-primary" role="alert" draggable="true" :data-index="index" :data-name="input" @dragstart="dragIO">
                      {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                    </div>
                  </li>
                </ul>
              </div>
              <div class="col-sm">
                <ul>
                  <li v-for="(input, index) in ios" v-if="index >= Math.ceil((curPageStartItem + curPageEndItem)/2)">
                    <div class="alert alert-primary" role="alert">
                      {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <!-- 模块显示区 -->
          <div class="col-sm-4">
            <module-selector
              :module-num="4"
              @modulesupdate="getModuleConfigInfo">
            </module-selector>
            <module-config
              :module-name="modules[curSelectedModuleSeq-1]">
            </module-config>
            <button class="btn btn-primary" @click="bar">change</button>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  import ModuleConfig from './ModuleConfig'
  import ModuleSelector from './ModuleSelector'

  // 规定一页最多显示的数据
  const pageItemAmount = 32;

  export default {
    components:{
      ModuleSelector,
      ModuleConfig
    },
    data(){
      return {
        ioType: 'di',
        ioNum: pageItemAmount,       // 初始化足够大的值，确保第一次请求的数据足够显示
        ios: {},
        curPage: 1,
        loading: true,

        ioForModule: {di1: '可编程io输入1', do1: '可编程io输出1'},
        modules: ['', '', '', ''],
        modulesIOs: [{}, {}, {}, {}],
        curSelectedModuleSeq: 1
      }
    },
    computed: {
      pages: function(){
        let pageAmount = Math.ceil( this.ioNum / pageItemAmount );
        let pgs = [];
        for(let i=1; i<= pageAmount; i++){
          pgs.push(i);
        }
        return pgs
      },
      curPageStartItem: function(){
        return 1 + (this.curPage - 1) * pageItemAmount
      },
      curPageEndItem: function(){
        return this.curPage * pageItemAmount < this.ioNum ? this.curPage * pageItemAmount : this.ioNum;
      }
    },
    methods: {
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
      getModuleConfigInfo(e){
        this.curSelectedModuleSeq = e.curSelected;
        for(let i=0; i<e.modules.length; i++){
          let moduleName = e.modules[i] === '未使用' ? '':e.modules[i];
          this.$set(this.modules, i, moduleName);
        }
      },
      bar(){
        this.$set(this.modulesIOs, [this.curSelectedModuleSeq-1], {'di1': '可编程输入1'});
        window.setTimeout(()=>{
          this.$set(this.modulesIOs, [this.curSelectedModuleSeq-1], {'di1': '可编程输入2'});
          console.log(this.modulesIOs);
        }, 2000);
      },
      dragIO(e){
        // 通过拖拽的方式向ModuleConfig.vue传递io信息，格式例如："di--1--阀门1开"
        e.dataTransfer.setData('ioInfo', this.ioType + '--' + e.target.getAttribute('data-index') + '--' + e.target.getAttribute('data-name'));
      },
    },
    watch: {
      ioType: function(newType, oldType){
        // 切换不同io页面需要重置this.ioNum，确保获取到足够多的数据
        this.ioNum = pageItemAmount;
        this.gotoPage(1)
      }
    },
    mounted() {
      this.gotoPage(this.curPage);
    }
  }
</script>
<style scoped lang='scss'>
  ul{
    list-style-type: none;
  }
  .nav{
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
  }
</style>
