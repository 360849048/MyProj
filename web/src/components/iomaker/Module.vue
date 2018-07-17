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
   * 4.当某插槽选为CAI888时，AJAX获取相应IO名称后，自动填充对应的IO配置加热1-8
   * 5.TODO：大机选配CIO021，自动填充对应的IO
   */
  import ModuleConfig from './module/ModuleConfig'
  import ModuleSelector from './module/ModuleSelector'

  export default {
    name: "module",
    props: ['bigImm'],
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
            if(allModules[this.curSelectedBoardSeq - 1][i] === 'CAI888'){
              // ajax获取TI和TO，填充默认的CAI888模块
              let cai888DefaultIos = {};
              let _this = this;
              $.when($.ajax({
                url: "/io",
                type: 'GET',
                dataType: 'json',
                beforeSend: function(){

                },
                complete: function(){

                },
                data: {"type": 'ti', "start": 1, 'end': 8},
                success: function(data){
                  for(let key in data.ios){
                    cai888DefaultIos['ti'+key] = key + '--'+ data.ios[key];
                  }
                },
                error: function(){
                  console.log('Error!!!');

                }
              }), $.ajax({
                url: "/io",
                type: 'GET',
                dataType: 'json',
                beforeSend: function(){

                },
                complete: function(){

                },
                data: {"type": 'to', "start": 1, 'end': 8},
                success: function(data){
                  for(let key in data.ios){
                    cai888DefaultIos['to'+key] = key + '--'+ data.ios[key];
                  }
                },
                error: function(){
                  console.log('Error!!!');

                }
              })).done(function(){
                _this.$set(allModulesIOs[_this.curSelectedBoardSeq - 1], i, cai888DefaultIos);
              });
            }else {
              // 其余模块清空IO配点信息
              this.$set(allModulesIOs[this.curSelectedBoardSeq - 1], i, {});
            }
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
