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
              :boardNum="2"
              :module-num="4"
              @modulesupdate="getModulesConfigInfo">
            </module-selector>
            <!-- 模块IO点显示 -->
            <module-config
              :module-name="modules[curSelectedModuleSeq-1]"
              :ios="modulesIOs[curSelectedModuleSeq-1]"
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
        modules: ['', '', '', ''],
        modulesIOs: [{}, {}, {}, {}],
        curSelectedModuleSeq: 1
      }
    },
    methods: {
      getModulesConfigInfo(e){
        this.curSelectedModuleSeq = e.curSelected;
        for(let i=0; i<e.modules.length; i++){
          let moduleName = e.modules[i] === '未使用' ? '':e.modules[i];
          if(this.modules[i] !== moduleName){
            this.$set(this.modules, i, moduleName);
            // 当某个插槽的模块检测到变化时，清空原先模块的IO信息
            this.$set(this.modulesIOs, i, {});
          }
        }
      },
      getModuleIoInfo(e){
        this.$set(this.modulesIOs, this.curSelectedModuleSeq-1, e);
      },
    },
  }
</script>
<style scoped lang='scss'>

</style>
