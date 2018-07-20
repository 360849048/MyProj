<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- IO选择区域 -->
          <transition name="fade-left">
            <div class="col-sm-4" v-show="curStep === 1">
              <form>
                <div class="form-group">
                  <label for="exampleFormControlInput1">Email address</label>
                  <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
                </div>
                <div class="form-group">
                  <label for="exampleFormControlSelect1">Example select</label>
                  <select class="form-control" id="exampleFormControlSelect1">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                    <option>5</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="exampleFormControlSelect2">Example multiple select</label>
                  <select multiple class="form-control" id="exampleFormControlSelect2">
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                    <option>5</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="exampleFormControlTextarea1">Example textarea</label>
                  <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
                </div>
              </form>
            </div>
          </transition>

          <div class="col-sm-8" >
            <io-list
            :boardModules1="boardModules1"
            :boardModules2="boardModules2"
            :boardModules="boardModules3"
            :boardModulesIOs1="boardModulesIOs1"
            :boardModulesIOs2="boardModulesIOs2"
            :boardModulesIOs3="boardModulesIOs3">
            </io-list>
          </div>
          <!-- 模块显示区 -->
          <transition name="fade-right">
            <div class="col-sm-4" id="module_area" v-show="curStep === 2" >
              <module
                :big-imm="true"
                @modulesupdate="getModuleInfo">
              </module>
            </div>
          </transition>
        </div>
        <!-- 测试按钮 -->
        <div class="row">
          <button @click="curStep=curStep===1?2:1">下一步</button>
        </div>
      </div>
    </div>
</template>
<script>
  import IoList from './iomaker/IoList'
  import Module from './iomaker/Module'

  export default {
    components:{
      IoList,
      Module
    },
    data(){
      return{
        // 格式如同： ['CDM163', 'CTO163', '', '']
        boardModules1: ['', '', '', ''],
        boardModules2: ['', '', '', ''],
        boardModules3: ['', '', '', ''],
        // 格式如下：[{'di1': '可编程IO输入1', 'do3': '43--阀门1'}]
        boardModulesIOs1: [{}, {}, {}, {}],
        boardModulesIOs2: [{}, {}, {}, {}],
        boardModulesIOs3: [{}, {}, {}, {}],

        curStep: 1
      }
    },
    methods:{
      getModuleInfo(e){
        for(let i=0; i<e.boardModules1.length; i++){
          if(e.boardModules1[i] !== this.boardModules1[i]){
            this.$set(this.boardModules1, i, e.boardModules1[i])
          }
        }
        for(let i=0; i<e.boardModules2.length; i++){
          if(e.boardModules2[i] !== this.boardModules2[i]){
            this.$set(this.boardModules2, i, e.boardModules2[i])
          }
        }
        for(let i=0; i<e.boardModules3.length; i++){
          if(e.boardModules3[i] !== this.boardModules3[i]){
            this.$set(this.boardModules3, i, e.boardModules3[i])
          }
        }
        this.boardModulesIOs1 = e.boardModulesIOs1;
        this.boardModulesIOs2 = e.boardModulesIOs2;
        this.boardModulesIOs3 = e.boardModulesIOs3;
      }
    }
  }
</script>
<style scoped>
  .fade-left-enter-active, .fade-left-leave-active{
    transition: all .5s ease;
  }
  .fade-left-enter, .fade-left-leave-to{
    opacity: 0;
    margin-left: -33.4%;
  }
  .fade-right-enter-active, .fade-right-leave-active{
    transition: all .5s ease;
  }
  .fade-right-enter, .fade-right-leave-to{
    opacity: 0;
    margin-right: -40%;
  }
</style>
