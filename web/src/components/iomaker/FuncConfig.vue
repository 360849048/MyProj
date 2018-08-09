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
        <transition name="fade">
          <form v-show="funcs[666].status">
            <label id="extHotrunnerLabel">外置热流道组数</label>
            <el-input-number :min="1" :max="10" label="热流道组数"
                             v-model="extHotrunnerNum"
                             @change="handleChange">
            </el-input-number>
          </form>
        </transition>
      </div>
      <div class="col-6">
        <h2>功能配置</h2>
        <h3 class="ml-3 mt-3 text-secondary">施工中...</h3>
      </div>
    </div>
  </div>
</template>

<script>
  /**
   * 获取主底板IO配置信息
   * TODO: 获取功能配置信息，POST到后台生成相应功能配置文件
   */
  import FuncSwitch from './funcConfig/FuncSwitch'
  export default {
    name: "function-config",
    components: {
      FuncSwitch
    },
    data(){
      return{
        funcs: {
          // 新增功能序号依次从小往大增加
          // 不要去修改外置热流道序号，极易出bug
          1: {name: '功能点1注射信号', status: false},
          2: {name: '功能点2储料信号', status: false},
          3: {name: 'E73', status: false},
          4: {name: '喷嘴改阀门1', status: false},
          5: {name: 'DEE能耗模块', status: false},
          666: {name: '外置热流道', status: false}
        },
        extHotrunnerNum: 3
      }
    },
    methods: {
      getFuncStatus(e){
        this.funcs[e.id].status = e.status;
        this.$emit('functionsupdate', this.funcs);
      },
      handleChange(){
        this.$emit('exthotrunnerchange', this.extHotrunnerNum);
      }
    },
  }
</script>

<style scoped>
  #funcconfig{
    /*border: 1px gray dotted;*/
  }
  #extHotrunnerLabel{
    margin-left: 3rem;
    display: inline-block;
    font-size: 1.2rem;
    width: 10rem;
  }
  .fade-enter-active, .fade-leave-active{
    transition: all .5s;
  }
  .fade-enter, .fade-leave-to{
    opacity: 0;
  }
</style>
