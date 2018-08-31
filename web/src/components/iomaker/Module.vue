<template>
  <div id="module">
    <module-selector
      :board-num="3"
      :board-slot-num="mainBoardSlotNum"
      :board1="boardModules1"
      :board2="boardModules2"
      :board3="boardModules3"
      @moduleselectupdate="getModulesSelectInfo">
    </module-selector>
    <!-- 模块IO点显示 -->
    <module-config
      :module-name="curActiveModule"
      :ios="curActiveModuleIOs"
      :new-io-to-append="newIoToAppend"
      :cur-board="curSelectedBoardSeq"
      @moduleiosupdate = "getModuleIoInfo"
      @varanposupdate = 'getVaranPos'>
    </module-config>
    <!-- 为了激活computed属性，从而触发modulesupdate事件 -->
    <div v-show="false">{{_emitData}}</div>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 1.处理并保存各底板模块配置及模块IO配置信息
   *   该组件与两个子组件的数据交换是双向的(模块选择及模块IO点位的配置)，即在此模块修改IO信息，数据将会传递下去并实时刷新视图
   *   从ModuleSelector获取模块的选择清单，以及当前选中的底板和模块信息
   *   将当前选中的模块以及当前模块的IO配置信息传递到ModuleConfig
   * 2.当某插槽选为CAI888时，AJAX获取相应IO名称后，自动填充对应的IO配置加热1-8
   * 3.自动初始化大机选配的CIO021(或CIO011)点位，通过AJAX方法从后台获取IO配点信息
   * 4.为了检测任意底板任意模块变动，在computed下的_emitData属性，通过modulesupdate事件将模块的选择及io配置信息传给父组件
   * 5.modulesupdate事件传递一个json格式如下:
   *      {
   *        'boardModules1': ['CIO021', 'CDM163', '', '']
   *        'boardModules2': ['CIV512', 'CAI888', '', '']
   *        'boardModules3': ['', '', '', '']
   *        'boardModulesIOs1': [{'di3': '83', 'do1': '97'}, {'di1': xxx}, {}, {}]
   *        'boardModulesIOs2': [{}, {}, {}, {}]
   *        'boardModulesIOs3': [{}, {}, {}, {}]
   *      }
   * 6.接收父组件传递过来的newIoToAppend，再将它传递给子组件ModuleConfig处理
   * 7.透传子组件ModuleConfig的varanposupdate事件，将以同名事件触发并传递数据到父组件
   * 注意：为了少动脑子，这里底板2和底板3的Varan连接模块顺序只能设置成一样，用到了底板3属于超特殊程序，不建议用这软件配置
   */
  import ModuleConfig from './module/ModuleConfig'
  import ModuleSelector from './module/ModuleSelector'

  function getBigImmStdIO(_this){
    /**
     * 通过ajax方法获取大机选配的IO点
     * 为了减少重复代码以及调用以及后期维护的方便，这里单独拎出来作为函数
     */
    if(_this.bigImm){
      $.ajax({
        url: '/big',
        type: 'GET',
        dataType: 'json',
        data: {"type": _this.type},
        success: (data) => {
          _this.$set(_this.boardModules1, 0, data.name);
          _this.$set(_this.boardModulesIOs1, 0, data.ios);
        },
        error: () => {
          console.log('AJAX获取大机配点信息失败');
        }
      });
    }else{
      _this.$set(_this.boardModules1, 0, '');
    }
  }
  export default {
    name: "module",
    props: ['bigImm', 'type', 'newIoToAppend'],
    components: {
      ModuleSelector,
      ModuleConfig
    },
    data() {
      return {
        // 格式如同： ['CDM163', 'CTO163', '', '']
        boardModules1: ['', '', '', ''],
        boardModules2: ['', '', '', ''],
        boardModules3: ['', '', '', ''],
        // 格式如下：[{'di1': '70--可编程IO输入1', 'do3': '43--阀门1'}]
        boardModulesIOs1: [{}, {}, {}, {}],
        boardModulesIOs2: [{}, {}, {}, {}],
        boardModulesIOs3: [{}, {}, {}, {}],
        curSelectedBoardSeq: 1,
        curSelectedModuleSeq: 1
      }
    },
    computed: {
      mainBoardSlotNum(){
        if(this.type.toUpperCase() === 'VE2'){
          // 清空主底板其余三块插槽的配置信息
          this.$set(this.boardModules1, 1, '');
          this.$set(this.boardModules1, 2, '');
          this.$set(this.boardModules1, 3, '');
          this.$set(this.boardModulesIOs1, 1, {});
          this.$set(this.boardModulesIOs1, 2, {});
          this.$set(this.boardModulesIOs1, 3, {});
          return 1;
        }
        return 4;
      },
      curActiveModule(){
        let allModules = [this.boardModules1, this.boardModules2, this.boardModules3];
        return allModules[this.curSelectedBoardSeq - 1][this.curSelectedModuleSeq - 1];
      },
      curActiveModuleIOs(){
        let allModulesIOs = [this.boardModulesIOs1, this.boardModulesIOs2, this.boardModulesIOs3];
        return allModulesIOs[this.curSelectedBoardSeq - 1][this.curSelectedModuleSeq - 1];
      },
      // _emitData用来向父组件发送消息，但必须在template中使用该属性才有效
      _emitData(){
        // 去除boardModulesIOs1中IO信息的冗余部分(去除IO点的中文名称，只留下IO的序号)
        let boardModulesIOs1 = JSON.parse(JSON.stringify(this.boardModulesIOs1));    // 深拷贝
        for(let moduleIOs of boardModulesIOs1){
          if(moduleIOs === {}){
            continue;
          }
          for(let key in moduleIOs){
            moduleIOs[key] = moduleIOs[key].split('--')[0]                            // 对对象的值进行了修改，为了不影响其他使用，上面进行了深拷贝
          }
        }
        let boardModulesIOs2 = JSON.parse(JSON.stringify(this.boardModulesIOs2));    // 深拷贝
        for(let moduleIOs of boardModulesIOs2){
          if(moduleIOs === {}){
            continue;
          }
          for(let key in moduleIOs){
            moduleIOs[key] = moduleIOs[key].split('--')[0]
          }
        }
        let boardModulesIOs3 = JSON.parse(JSON.stringify(this.boardModulesIOs3));    // 深拷贝
        for(let moduleIOs of boardModulesIOs3){
          if(moduleIOs === {}){
            continue;
          }
          for(let key in moduleIOs){
            moduleIOs[key] = moduleIOs[key].split('--')[0]
          }
        }
        this.$emit('modulesupdate', {
          'boardModules1': this.boardModules1,
          'boardModules2': this.boardModules2,
          'boardModules3': this.boardModules3,
          'boardModulesIOs1': boardModulesIOs1,
          'boardModulesIOs2': boardModulesIOs2,
          'boardModulesIOs3': boardModulesIOs3,
        });
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
              // AJAX获取TI和TO，填充默认的CAI888模块
              // 这里仍旧使用了IoList的接口，性能较差，
              // TODO：后端单独开一个api用以获取CAI888，可以提高性能
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
                // 这里定义了CAI888模块的配点信息为TI的1-8号点，AJAX仅仅用于获取1-8点对应的名称
                data: {"type": 'ti', "start": 1, 'end': 8},
                success: function(data){
                  for(let key in data.ios){
                    cai888DefaultIos['ti'+key] = key + '--'+ data.ios[key];
                  }
                },
                error: function(){
                  console.log('AJAX获取CAI888的TI名称失败');
                }
              }), $.ajax({
                url: "/io",
                type: 'GET',
                dataType: 'json',
                beforeSend: function(){

                },
                complete: function(){

                },
                // 这里定义了CAI888模块的配点信息为TO的1-8号点，AJAX仅仅用于获取1-8点对应的名称
                data: {"type": 'to', "start": 1, 'end': 8},
                success: function(data){
                  for(let key in data.ios){
                    cai888DefaultIos['to'+key] = key + '--'+ data.ios[key];
                  }
                },
                error: function(){
                  console.log('AJAX获取CAI888的TO名称失败');
                }
              })).done(function(){
                _this.$set(allModulesIOs[_this.curSelectedBoardSeq - 1], i, cai888DefaultIos);
              });
            }else if(this.bigImm && this.curSelectedBoardSeq === 1 && this.curSelectedModuleSeq === 1){
              // 修复了bug：大机情况下无法重置底板一的模块信息
              if( (this.type.toUpperCase() === 'VE2' && this.boardModules1[0] === 'CIO011') ||
                (this.type.toUpperCase() !== 'VE2' && this.boardModules1[0] === 'CIO021') ){
                getBigImmStdIO(this);
              }else{
                this.$set(allModulesIOs[this.curSelectedBoardSeq - 1], i, {});
              }
            }else{
              // 当模块选择发生变动时，除上述两种情况外，清空这个模块的配点信息
              this.$set(allModulesIOs[this.curSelectedBoardSeq - 1], i, {});
            }
          }
        }
      },
      getModuleIoInfo(e){
        let allModulesIOs = [this.boardModulesIOs1, this.boardModulesIOs2, this.boardModulesIOs3];
        this.$set(allModulesIOs[this.curSelectedBoardSeq - 1], this.curSelectedModuleSeq - 1, e);
      },
      getVaranPos(e){
        this.$emit('varanposupdate', e);
      }
    },
    watch: {
      bigImm(){
        getBigImmStdIO(this);
      },
      type(){
        getBigImmStdIO(this);
      }
    },
  }
</script>

<style scoped>

</style>
