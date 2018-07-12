<template>
  <div id="module-selector">
    <!-- 主底板&扩展底板一 -->
    <ul class="nav nav-tabs">
      <li class="nav-item" v-for="boardSeq in boardNum" @click="curSelectedBoard=boardSeq">
        <a class="nav-link" :class="{'active': curSelectedBoard===boardSeq}" href="#">{{boards[boardSeq-1]}}</a>
      </li>
    </ul>
    <!-- 插槽模块选择 -->
    <div class="btn-group btn-group-toggle" data-toggle="buttons">
      <!-- 主底板 -->
      <div class="btn-group" v-for="moduleSeq in moduleNum" v-if="curSelectedBoard===1 && moduleNum >= 1">
        <button type="button" class="btn btn-secondary btn-sm btn-module-name"
                :class="{'active': curSelectedModuleSeq===moduleSeq}"
                v-model="modules[moduleSeq-1]"
                @click="clickOnModuleBtn(moduleSeq)">
          {{modules[moduleSeq-1]}}
        </button>
        <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <span class="sr-only">Toggle Dropdown</span>
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#"
             v-for="(module, index) in moduleLib"
             @click="clickOnSelectBtn(moduleSeq, index)">
            {{module}}
          </a>
        </div>
      </div>
      <!-- 扩展底板一 -->
    </div>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 1.根据props属性moduleNum显示插槽数量（HTML模板列表渲染）
   * 2.鼠标单击某个模块或选择新模块，都会触发modulesupdate事件，向父组件传递当前应当显示的模块以及各插槽应配置的模块
   */
    export default {
      name: "module-selector",
      props: ['boardNum', 'moduleNum'],
      data(){
        return{
          // 更新数组内容请使用：vm.$set(vm.items, indexOfItem, newValue)
          boards: ['主底板', '底板二'],
          curSelectedBoard: 1,
          modules: ['未使用', '未使用', '未使用', '未使用'],
          curSelectedModuleSeq: 1,
          moduleLib: ['未使用', 'CIO021', 'CDM163', 'CTO163', 'CDI163', 'CAI888']
        }
      },
      methods: {
        clickOnModuleBtn(moduleSeq){
          this.curSelectedModuleSeq = moduleSeq;
          this.$emit('modulesupdate', {curSelected: this.curSelectedModuleSeq, modules: this.modules});
        },
        clickOnSelectBtn(moduleSeq, index){
          this.$set(this.modules, moduleSeq-1, this.moduleLib[index]);
          this.$emit('modulesupdate', {curSelected: this.curSelectedModuleSeq, modules: this.modules});
        }
      }
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
