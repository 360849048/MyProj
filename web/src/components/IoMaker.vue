<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- IO选择区域 -->
          <div class="col-sm-8">
            <io-list
            :boardModules1="boardModules1"
            :boardModules2="boardModules2"
            :boardModules="boardModules3"
            :boardModulesIOs1="boardModulesIOs1"
            :boardModulesIOs2="boardModulesIOs2"
            :boardModulesIOs3="boardModulesIOs3">
            </io-list>
          </div>
          <!-- 模块显示区 -->
          <div class="col-sm-4" id="module_area">
            <module
              :big-imm="true"
              @modulesupdate="getModuleInfo">
            </module>
          </div>
        </div>
        <ul class="dataarea">
          <li>{{boardModules1}}--{{boardModulesIOs1}}</li>
          <li>{{boardModules2}}--{{boardModulesIOs2}}</li>
          <li>{{boardModules3}}--{{boardModulesIOs3}}</li>
        </ul>
      </div>
    </div>
</template>
<script>
  import IoList from './iomaker/IoList'
  import Module from './iomaker/Module'

  export default {
    components:{
      IoList,
      Module
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
<style scoped>

</style>
