<template>
  <div id="funcconfig">
    <div class="row">
      <div class="col-4">
        <h2>主底板默认IO修改</h2>
        <div v-for="(item, index) in funcs" class="p-1">
          <func-switch
            :id="index"
            :name="item.name"
            :status="item.status"
            @statusupdate="getFuncStatus">
          </func-switch>
        </div>
      </div>
      <div class="col-6">
        <h2>功能配置</h2>
        <h3 class="ml-3 mt-3">施工中...</h3>
      </div>
    </div>
  </div>
</template>

<script>
  import FuncSwitch from './funcConfig/FuncSwitch'
  export default {
    name: "function-config",
    components: {
      FuncSwitch
    },
    data(){
      return{
        funcs: {
          1: {name: '功能点1注射信号', status: false},
          2: {name: '功能点2储料信号', status: false},
          3: {name: 'E73', status: false},
          4: {name: '喷嘴改阀门1', status: false}
        }
      }
    },
    methods: {
      getFuncStatus(e){
        this.funcs[e.id].status = e.status;
      }
    }
  }
</script>

<style scoped>
  #funcconfig{
    /*border: 1px gray dotted;*/
  }
</style>
