<template>
  <div id="module">
    <module-selector
      :board-num="3"
      :board-slot-num="4"
      @modulesupdate="getModulesSelectInfo">
    </module-selector>
    <!-- 模块IO点显示 -->
    <module-config
      :module-name="curActiveModule"
      :ios="curActiveModuleIOs"
      @moduleiosupdate = "getModuleIoInfo">
    </module-config>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 1.处理并保存各底板模块配置及模块IO配置信息
   * 2.从ModuleSelector获取模块的选择清单，以及当前选中的底板和模块信息
   * 3.将当前选中的模块以及当前模块的IO配置信息传递到ModuleConfig
   * 4.当某插槽选为CAI888时，自动填充对应的IO配置加热1-8
   */
  import ModuleConfig from './module/ModuleConfig'
  import ModuleSelector from './module/ModuleSelector'
  export default {
    name: "module",
    components: {
      ModuleSelector,
      ModuleConfig
    },
    data() {
      return {
        // 格式如同： ['CDM163', 'CTO163']
        boardModules1: ['', '', '', ''],
        boardModules2: ['', '', '', ''],
        boardModules3: ['', '', '', ''],
        // 格式如下：[{'di1': '可编程IO输入1', 'do3': '43--阀门1'}]
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
      getModulesSelectInfo(e){
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

<style scoped>

</style>
