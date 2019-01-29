<template>
  <div id="funcconfig">
    <div class="row">
      <div class="col-xl-6">
        <h2>IO表相关修改</h2>
        <hr>
        <!-- v-if里面不能用 === -->
        <div v-for="(item, index) in funcs" v-if="index <= 100" class="p-1">
          <func-switch
            :id="index"
            :name="item.name"
            :status="item.status"
            @statusupdate="getFuncStatus">
          </func-switch>
        </div>
        <transition name="fade">
          <form v-show="funcs[99].status">
            <label id="extHotrunnerLabel">外置热流道组数</label>
            <el-input-number :min="1" :max="10" label="热流道组数"
                             v-model="extHotrunnerNum"
                             @change="handleExtHot">
            </el-input-number>
          </form>
        </transition>
      </div>
      <div class="col-xl-6">
        <h2>功能配置</h2>
        <hr>
        <!--<h3 class="ml-3 mt-3 text-secondary">施工中...</h3>-->
        <form>
          <label id="intHotrunnerLabel">内置热流道组数</label>
          <el-input-number :min="0" :max="2" label="热流道组数"
                           v-model="intHotrunnerNum"
                           @change="handleIntHot">
          </el-input-number>
        </form>
        <div v-for="(item, index) in funcs" v-if="index > 100" class="p-1">
          <func-switch
            :id="index"
            :name="item.name"
            :status="item.status"
            @statusupdate="getFuncStatus">
          </func-switch>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 该模块集中处理一些功能开关，所有功能的开闭信息都由this.funcs保管。
   * 每次增加或删除某个具体功能，需要看情况修改父组件、后端的代码（尤其是涉及到IO点修改的功能，必须谨慎处理，防止影响到其他功能）
   * 该模块可触发以下几种事件：
   *  * functionsupdate：当功能的开闭状态发生变化时，触发该事件
   *  * exthotrunnerchange：当外置热流道组数设置发生变化时，触发该事件
   *  * inthotrunnerchange：内置热流道组数设置发生变化时，触发该事件
   */
  import FuncSwitch from './FuncSwitch'
  export default {
    name: "function-config",
    components: {
      FuncSwitch
    },
    props: ['type'],
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
          6: {name: '7号改可编程输入1', status: false},
          7: {name: '功能点1改可编程输出1', status: false},
          8: {name: '功能点2改可编程输出2', status: false},
          98: {name: 'PSG热流道', status: false},
          99: {name: '外置热流道', status: false},
          101: {name: '阀门', status: false},
          102: {name: '吹气', status: false},
          103: {name: '中子', status: false},
          104: {name: '可编程IO', status: false}
        },
        extHotrunnerNum: 3,
        intHotrunnerNum: 0
      }
    },
    methods: {
      getFuncStatus(e){
        this.funcs[e.id].status = e.status;
        this.$emit('functionsupdate', this.funcs);
      },
      handleExtHot(){
        this.$emit('exthotrunnerchange', this.extHotrunnerNum);
      },
      handleIntHot(){
        this.$emit('inthotrunnerchange', this.intHotrunnerNum);
      }
    },
    watch:{
      funcs:{
        handler: function(cval){
          if(this.type === 'VE2' && cval[3].status){
            this.$message({
              message: 'VE2机器的E73两个输入点需要自行配置',
              type: 'warning'
            });
          }
          if(cval[6].status && this.type === 'VE2') {
            this.funcs[6].status = false;
            this.$message({
              message: 'VE2机器不支持7号点的修改',
              type: 'error'
            });
          }
          if(cval[3].status && cval[6].status){
            this.funcs[6].status = false;
            this.$message({
              message: 'E73已经修改了输入7号点，不可重复配置',
              type: 'error'
            });
          }
          if(cval[7].status && cval[1].status){
            this.funcs[7].status = false;
            this.$message({
              message: '请将可编程IO输出1配到模块',
              type: 'warning'
            });
          }
          if(cval[8].status && cval[2].status){
            this.funcs[8].status = false;
            this.$message({
              message: '请将可编程IO输出2配到模块',
              type: 'warning'
            });
          }
          if(cval[98].status && cval[99].status){
            this.funcs[99].status = false;
            this.$message({
              message: 'PSG热流道只需要SE051，不需要额外的CAI888',
              type: 'warning'
            });
          }
        },
        deep: true,
      }
    }
  }
</script>

<style scoped lang="scss">
  #funcconfig{
    /*border: 1px gray dotted;*/
    /* 设置一定的padding，消除底部滚动条 */
    padding: 15px;
    box-sizing: border-box;
    height: 100%;
    overflow: auto;
    &::-webkit-scrollbar{
      width: 6px;
      height: 6px;
     }
    &::-webkit-scrollbar-thumb{
       border-radius: 10px;
       -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
       background: #818080;
     }
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
