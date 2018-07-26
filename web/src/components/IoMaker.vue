<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- 信息录入 -->
          <transition name="fade-left">
            <div class="col-sm-4" v-show="curStep === 1">
              <info-form>
              </info-form>
            </div>
          </transition>
          <!-- 功能配置 -->
          <transition name="vanish-left">
            <div class="col-sm-8" v-show="curStep === 1">
              <func-config>
              </func-config>
            </div>
          </transition>
          <!-- IO选择区域 -->
          <transition name="vanish-right">
            <div class="col-sm-8" v-show="curStep === 2">
              <io-list
                :boardModules1="boardModules1"
                :boardModules2="boardModules2"
                :boardModules="boardModules3"
                :boardModulesIOs1="boardModulesIOs1"
                :boardModulesIOs2="boardModulesIOs2"
                :boardModulesIOs3="boardModulesIOs3">
              </io-list>
            </div>
          </transition>
          <!-- 模块显示区 -->
          <transition name="fade-right">
            <div class="col-sm-4" id="module_area" v-show="curStep === 2" >
              <module
                :big-imm="true"
                @modulesupdate="getModuleInfo">
              </module>
            </div>
          </transition>
        </div>
        <!-- 测试按钮 -->
        <!--<div class="row">-->
          <!--<button @click="curStep=curStep===1?2:1" class="btn btn-success">下一步</button>-->
        <!--</div>-->
      </div>
      <footer class="fixed-bottom text-center">
        <i class="fa fa-angle-left fa-4x" aria-hidden="true" @click="curStep=1"></i>
        <a href="#" class="fa-3x">提交</a>
        <i class="fa fa-angle-right fa-4x" aria-hidden="true" @click="curStep=2"></i>
      </footer>
    </div>
</template>
<script>
  import IoList from './iomaker/IoList'
  import Module from './iomaker/Module'
  import InfoForm from './iomaker/infoForm'
  import FuncConfig from './iomaker/FuncConfig'

  export default {
    components:{
      IoList,
      Module,
      InfoForm,
      FuncConfig
    },
    data(){
      return{
        // 格式如同： ['CDM163', 'CTO163', '', '']
        boardModules1: ['', '', '', ''],
        boardModules2: ['', '', '', ''],
        boardModules3: ['', '', '', ''],
        // 格式如下：[{'di1': '可编程IO输入1', 'do3': '43--阀门1'}]
        boardModulesIOs1: [{}, {}, {}, {}],
        boardModulesIOs2: [{}, {}, {}, {}],
        boardModulesIOs3: [{}, {}, {}, {}],

        curStep: 1
      }
    },
    methods:{
      getModuleInfo(e){
        for(let i=0; i<e.boardModules1.length; i++){
          if(e.boardModules1[i] !== this.boardModules1[i]){
            this.$set(this.boardModules1, i, e.boardModules1[i])
          }
        }
        for(let i=0; i<e.boardModules2.length; i++){
          if(e.boardModules2[i] !== this.boardModules2[i]){
            this.$set(this.boardModules2, i, e.boardModules2[i])
          }
        }
        for(let i=0; i<e.boardModules3.length; i++){
          if(e.boardModules3[i] !== this.boardModules3[i]){
            this.$set(this.boardModules3, i, e.boardModules3[i])
          }
        }
        this.boardModulesIOs1 = e.boardModulesIOs1;
        this.boardModulesIOs2 = e.boardModulesIOs2;
        this.boardModulesIOs3 = e.boardModulesIOs3;
      }
    }
  }
</script>
<style lang="scss" scoped>
  .fade-left-enter-active, .fade-left-leave-active{
    transition: all .5s ease;
  }
  .fade-left-enter, .fade-left-leave-to{
    opacity: 0;
    margin-left: -33.4%;
  }
  .fade-right-enter-active, .fade-right-leave-active{
    transition: all .5s ease;
  }
  .fade-right-enter, .fade-right-leave-to{
    opacity: 0;
    margin-right: -40%;
  }
  .vanish-left-enter-active, .vanish-left-leave-active{
    transition: all .5s ease;
  }
  .vanish-left-enter, .vanish-left-leave-to{
    opacity: 0;
    margin-left: -66.7%
  }
  .vanish-right-enter-active, .vanish-right-leave-active{
    transition: all .5s ease;
  }
  .vanish-right-enter, .vanish-right-leave-to{
    opacity: 0;
    margin-right: -66.7%;
  }
  footer{
    background-color: #eee;
    i{
      color: #666;
      cursor: pointer;
    }
    a{
      margin: 50px;
      text-decoration: none;
      color: #666;
    }
  }
</style>
