<template>
  <div id="module-selector">
    <!-- 主底板&扩展底板一 -->
    <ul class="nav nav-tabs">
      <li class="nav-item" v-for="boardSeq in boardNum" @click="clickOnBoardBtn(boardSeq)">
        <a class="nav-link" :class="{'active': curSelectedBoardSeq===boardSeq}" href="#">{{boards[boardSeq-1]}}</a>
      </li>
    </ul>
    <!-- 插槽模块选择 -->
    <div class="btn-group btn-group-toggle" data-toggle="buttons">
      <!-- 主底板 -->
      <div class="btn-group" v-for="moduleSeq in boardSlotNum" v-if="curSelectedBoardSeq===1">
        <button type="button" class="btn btn-secondary btn-sm btn-module-name"
                :class="{'active': curSelectedModuleSeq===moduleSeq}"
                @click="clickOnModuleBtn(moduleSeq)">
          {{boardModules1[moduleSeq-1]}}
        </button>
        <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <span class="sr-only">Toggle Dropdown</span>
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#"
             v-for="(module, index) in diasModules"
             @click="clickOnSelectDiasModuleBtn(moduleSeq, index)">
            {{module}}
          </a>
        </div>
      </div>
      <!-- 扩展底板一 -->
      <div class="btn-group" v-for="moduleSeq in 4" v-if="curSelectedBoardSeq===2">
        <button type="button" class="btn btn-secondary btn-sm btn-module-name"
                :class="{'active': curSelectedModuleSeq===moduleSeq,}"
                @click="clickOnModuleBtn(moduleSeq)">
          {{boardModules2[moduleSeq-1]}}
        </button>
        <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <span class="sr-only">Toggle Dropdown</span>
        </button>
        <div class="dropdown-menu" v-if="moduleSeq===1">
          <a class="dropdown-item" href="#"
             v-for="(module, index) in connModules"
             @click="clickOnSelectConnModuleBtn(moduleSeq, index)">
            {{module}}
          </a>
        </div>
        <div class="dropdown-menu" v-if="moduleSeq>=2">
          <a class="dropdown-item" href="#"
             v-for="(module, index) in diasModules"
             @click="clickOnSelectDiasModuleBtn(moduleSeq, index)">
            {{module}}
          </a>
        </div>
      </div>
      <!-- 扩展底板二 -->
      <div class="btn-group" v-for="moduleSeq in 4" v-if="curSelectedBoardSeq===3">
        <button type="button" class="btn btn-secondary btn-sm btn-module-name"
                :class="{'active': curSelectedModuleSeq===moduleSeq}"
                @click="clickOnModuleBtn(moduleSeq)">
          {{boardModules3[moduleSeq-1]}}
        </button>
        <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <span class="sr-only">Toggle Dropdown</span>
        </button>
        <div class="dropdown-menu" v-if="moduleSeq===1">
          <a class="dropdown-item" href="#"
             v-for="(module, index) in connModules"
             @click="clickOnSelectConnModuleBtn(moduleSeq, index)">
            {{module}}
          </a>
        </div>
        <div class="dropdown-menu" v-if="moduleSeq>=2">
          <a class="dropdown-item" href="#"
             v-for="(module, index) in diasModules"
             @click="clickOnSelectDiasModuleBtn(moduleSeq, index)">
            {{module}}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 1.props属性boardSlotNum显示主底板插槽数量，不可超过4，扩展底板的插槽数量一律规定是4，这与父组件耦合!不可轻易修改插槽数量。
   * 2.props属性boardNum显示底板数量，不可超过3块。
   * 3.鼠标单击某个底板或某个模块或选择新模块，都会触发moduleselectupdate事件，向父组件传递当前应当显示的模块以及各插槽应配置的模块。
   * 4.moduleselectupdate事件传递一个json格式如下:
   *       {
   *         curSelectedBoardSeq: 1,
   *         curSelectedModuleSeq: 1,
   *         modules: ['未使用', 'xxx', 'xxx', 'xxx']
   *       }
   * 5.扩展底板的在配置前必须首先选择连接模块，否则无法选择第二块及以后的模块
   */
  export default {
    name: "module-selector",
    props: ['boardNum', 'boardSlotNum', 'board1', 'board2', 'board3'],
    data(){
      return{
        // 更新数组内容请使用：vm.$set(vm.items, indexOfItem, newValue)
        boards: ['主底板', '底板二', '底板三'],
        boardModules1: ['未使用', '未使用', '未使用', '未使用'],
        boardModules2: ['未使用', '未使用', '未使用', '未使用'],
        boardModules3: ['未使用', '未使用', '未使用', '未使用'],
        connModules: ['未使用', 'CIV512', 'CIV521'],
        diasModules: ['未使用', 'CIO021', 'CDM163', 'CTO163', 'CDI163', 'CAI888', 'CIO011'],
        curSelectedBoardSeq: 1,
        curSelectedModuleSeq: 1,
      }
    },
    methods: {
      _emit(_this){
        let allModules = [_this.boardModules1, _this.boardModules2, _this.boardModules3];
        _this.$emit('moduleselectupdate', {
          curSelectedBoardSeq: _this.curSelectedBoardSeq,
          curSelectedModuleSeq: _this.curSelectedModuleSeq,
          modules: allModules[_this.curSelectedBoardSeq - 1]
        });
      },
      clickOnBoardBtn(boardSeq){
        this.curSelectedBoardSeq = boardSeq;
        this.curSelectedModuleSeq = 1;
        this._emit(this);
      },
      clickOnModuleBtn(moduleSeq){
        this.curSelectedModuleSeq = moduleSeq;
        this._emit(this);
      },
      clickOnSelectDiasModuleBtn(moduleSeq, index){
        let allModules = [this.boardModules1, this.boardModules2, this.boardModules3];
        if(this.curSelectedBoardSeq > 1){
          // 当前在扩展底板时，需要首先配置连接模块
          if(allModules[this.curSelectedBoardSeq - 1][0] === '未使用'){
            this.$notify.error({
              title: '错误',
              message: '请先配置连接模块'
            });
            return;
          }
        }
        this.$set(allModules[this.curSelectedBoardSeq - 1], moduleSeq - 1, this.diasModules[index]);
        this._emit(this);
      },
      clickOnSelectConnModuleBtn(moduleSeq, index){
        let allModules = [this.boardModules1, this.boardModules2, this.boardModules3];
        this.$set(allModules[this.curSelectedBoardSeq - 1], moduleSeq - 1, this.connModules[index]);
        if(allModules[this.curSelectedBoardSeq - 1][0] === '未使用'){
          // 当连接模块取消后，清空后面的模块配置
          this.$set(allModules[this.curSelectedBoardSeq - 1], 1, '未使用');
          this.$set(allModules[this.curSelectedBoardSeq - 1], 2, '未使用');
          this.$set(allModules[this.curSelectedBoardSeq - 1], 3, '未使用');
        }
        this._emit(this);
      }
    },
    watch:{
      board1(cval){
        for(let i=0; i<cval.length; i++){
          let curModule = cval[i] === '' ? '未使用' : cval[i];
          if(curModule !== this.boardModules1[i]){
            this.$set(this.boardModules1, i, curModule);
          }
        }
      },
      board2(cval){
        for(let i=0; i<cval.length; i++){
          let curModule = cval[i] === '' ? '未使用' : cval[i];
          if(curModule !== this.boardModules2[i]){
            this.$set(this.boardModules2, i, curModule);
          }
        }
      },
      board3(cval){
        for(let i=0; i<cval.length; i++){
          let curModule = cval[i] === '' ? '未使用' : cval[i];
          if(curModule !== this.boardModules3[i]){
            this.$set(this.boardModules3, i, curModule);
          }
        }
      }
    },
  }
</script>

<style scoped lang="scss">
  .nav{
    margin: 10px;
    .nav-item{
      width: 100px;
      text-align: center;
    }
  }
  .btn-module-name{
    width: 70px;
  }
</style>
