<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- IO选择区域 -->
          <div class="col-sm-8">
            <io-list/>
          </div>
          <!-- 模块显示区 -->
          <div class="col-sm-4" id="module_area">
            <!-- 插槽模块选择 -->
            <module-selector
              :board-num="3"
              :board-slot-num="4"
              @modulesupdate="getModulesConfigInfo">
            </module-selector>
            <!-- 模块IO点显示 -->
            <module-config
              :module-name="curActiveModule"
              :ios="curActiveModuleIOs"
              @moduleiosupdate = "getModuleIoInfo">
            </module-config>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  import IoList from './iomaker/IoList'
  import ModuleConfig from './iomaker/ModuleConfig'
  import ModuleSelector from './iomaker/ModuleSelector'

  export default {
    components:{
      IoList,
      ModuleSelector,
      ModuleConfig
    },
    data() {
      return {
        // 格式如同： ['CDM163', 'CTO163']
        boardModules1: ['', '', '', ''],
        boardModules2: ['', '', '', ''],
        boardModules3: ['', '', '', ''],
        // 格式如下：[{'di1': '可编程IO输入1', 'do3': '阀门1'}]
        boardModulesIOs1: [{}, {}, {}, {}],
        boardModulesIOs2: [{}, {}, {}, {}],
        boardModulesIOs3: [{}, {}, {}, {}],
        curSelectedBoardSeq: 1,
        curSelectedModuleSeq: 1
      }
    },
    computed: {
      curActiveModule(){
        let allModules = [this.boardModules1, this.boardModules2, this.boardModules3];
        return allModules[this.curSelectedBoardSeq - 1][this.curSelectedModuleSeq - 1];
      },
      curActiveModuleIOs(){
        let allModulesIOs = [this.boardModulesIOs1, this.boardModulesIOs2, this.boardModulesIOs3];
        return allModulesIOs[this.curSelectedBoardSeq - 1][this.curSelectedModuleSeq - 1];
      }
    },
    methods: {
      getModulesConfigInfo(e){
        // console.log(e);
        this.curSelectedBoardSeq = e.curSelectedBoardSeq;
        this.curSelectedModuleSeq = e.curSelectedModuleSeq;
        let allModules = [this.boardModules1, this.boardModules2, this.boardModules3];
        let allModulesIOs = [this.boardModulesIOs1, this.boardModulesIOs2, this.boardModulesIOs3];

        for(let i=0; i<e.modules.length; i++){
          let moduleName = e.modules[i] === '未使用' ? '':e.modules[i];
          if(allModules[this.curSelectedBoardSeq - 1][i] !== moduleName){
            this.$set(allModules[this.curSelectedBoardSeq - 1], i, moduleName);
            // 当某个插槽的模块检测到变化时，清空原先模块的IO信息
            this.$set(allModulesIOs[this.curSelectedBoardSeq - 1], i, {});
          }
        }
      },
      getModuleIoInfo(e){
        let allModulesIOs = [this.boardModulesIOs1, this.boardModulesIOs2, this.boardModulesIOs3];
        this.$set(allModulesIOs[this.curSelectedBoardSeq - 1], this.curSelectedModuleSeq - 1, e);
      },
    },
  }
</script>
<style scoped lang='scss'>

</style>
