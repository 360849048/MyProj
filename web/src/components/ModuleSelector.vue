<template>
    <div class="btn-group btn-group-toggle" data-toggle="buttons" v-if="moduleNum >= 1">
      <div class="btn-group" v-for="moduleSeq in moduleNum" v-if="moduleNum >= moduleSeq">
        <button type="button" class="btn btn-secondary btn-sm btn-module-name"
                :class="{active: curSelectedModuleSeq===moduleSeq}"
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
    </div>
</template>

<script>
    export default {
      name: "module-selector",
      props: ['moduleNum'],
      data(){
        return{
          // 更新数组内容请使用：vm.$set(vm.items, indexOfItem, newValue)
          modules: ['未使用', '未使用', '未使用', '未使用'],
          curSelectedModuleSeq: 1,
          moduleLib: ['未使用', 'CIO021', 'CDM163', 'CTO163', 'CAI888']
        }
      },
      methods: {
        clickOnModuleBtn(moduleSeq){
          this.curSelectedModuleSeq = moduleSeq;
          // todo: 向父组件发送当前选中的插槽和各插槽配置的模块
          this.$emit('modulesupdate', {curSelected: this.curSelectedModuleSeq, modules: this.modules});
        },
        clickOnSelectBtn(moduleSeq, index){
          this.$set(this.modules, moduleSeq-1, this.moduleLib[index]);
          this.$emit('modulesupdate', {curSelected: this.curSelectedModuleSeq, modules: this.modules});
        }
      }
    }
</script>

<style scoped>
  .btn-module-name{
    width: 70px;
  }
</style>
