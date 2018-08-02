<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- 信息录入 -->
          <transition name="fade-left">
            <div class="col-sm-4" v-show="curStep === 1">
              <info-form
                @imminfochange="getImmInfo">
              </info-form>
            </div>
          </transition>
          <!-- 功能配置 -->
          <transition name="vanish-left">
            <div class="col-sm-8" v-show="curStep === 1">
              <func-config>
              </func-config>
            </div>
          </transition>
          <!-- IO选择区域 -->
          <transition name="vanish-right">
            <div class="col-sm-8" v-show="curStep === 2">
              <io-list
                :boardModules1="boardModules1"
                :boardModules2="boardModules2"
                :boardModules="boardModules3"
                :boardModulesIOs1="boardModulesIOs1"
                :boardModulesIOs2="boardModulesIOs2"
                :boardModulesIOs3="boardModulesIOs3">
              </io-list>
            </div>
          </transition>
          <!-- 模块显示区 -->
          <transition name="fade-right">
            <div class="col-sm-4" id="module_area" v-show="curStep === 2" >
              <module
                :big-imm="isBigImm"
                :type="type"
                @modulesupdate="getModuleInfo">
              </module>
            </div>
          </transition>
        </div>
      </div>
      <footer class="fixed-bottom">
        <i class="fa fa-angle-left fa-3x" :class="{'enable': curStep !== 1}" aria-hidden="true" @click="curStep=1"></i>
        <a href="#" class="fa-2x enable" @click="submitInfo">提交</a>
        <i class="fa fa-angle-right fa-3x" :class="{'enable': curStep !== 2}" aria-hidden="true" @click="curStep=2"></i>
      </footer>
    </div>
</template>
<script>
  /**
   * 数据处理逻辑：
   * 1.从infoForm收集机器基础信息，并根据immType解析机器具体参数信息：机器类型、单双注射、大机选配
   * 2.从FuncForm获取主底板IO修改信息：功能点12的配置等信息。TODO:功能配置文件信息录入
   * 3.从Module获取模块和模块上的IO配置信息，并将配置信息传递到IoList组件
   * 4.页脚处放置的一些按钮，用来移动展示页面以及向后台POST机器信息
   */

  import IoList from './iomaker/IoList'
  import Module from './iomaker/Module'
  import InfoForm from './iomaker/InfoForm'
  import FuncConfig from './iomaker/FuncConfig'

  export default {
    components:{
      IoList,
      Module,
      InfoForm,
      FuncConfig
    },
    data(){
      return{
        // 格式如同： ['CDM163', 'CTO163', '', '']
        boardModules1: ['', '', '', ''],
        boardModules2: ['', '', '', ''],
        boardModules3: ['', '', '', ''],
        // 格式如下：[{'di1': '70', 'do3': '43'}]
        boardModulesIOs1: [{}, {}, {}, {}],
        boardModulesIOs2: [{}, {}, {}, {}],
        boardModulesIOs3: [{}, {}, {}, {}],
        // 机器基础信息
        evaluationNum: '',
        productionNum: '',
        immType: '',
        customer: '',
        safetyStandard: '',
        technicalClause: '',
        designNote: '',
        // 解析immType后得到的数据
        isBigImm: false,
        isDualInj: false,
        clampForce: 0,
        injection: 0,
        type: '',

        // 控制页面的展示内容：信息录入 或 IO选配（左右移动）
        curStep: 1
      }
    },
    methods:{
      getImmInfo(e){
        this.evaluationNum = e.evaluationNum;
        this.productionNum = e.productionNum;
        this.immType = e.immType;
        this.customer = e.customer;
        this.safetyStandard = e.safetyStandard;
        this.technicalClause = e.technicalClause;
        this.designNote = e.designNote;
      },
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
      },
      submitInfo(){
        let dataToPost = {
          boardModules1: this.boardModules1,
          boardModules2: this.boardModules2,
          boardModules3: this.boardModules3,
          boardModulesIOs1: this.boardModulesIOs1,
          boardModulesIOs2: this.boardModulesIOs2,
          boardModulesIOs3: this.boardModulesIOs3,
          evaluationNum: this.evaluationNum,
          productionNum: this.productionNum,
          immType: this.immType,
          customer: this.customer,
          safetyStandard: this.safetyStandard,
          technicalClause: this.technicalClause,
          designNote: this.designNote,
          isBigImm: this.isBigImm,
          isDualInj: this.isDualInj,
          clampForce: this.clampForce,
          injection: this.injection,
          type: this.type
        };
        $.ajax({
          type: 'POST',
          url: '/iomaker',
          data: JSON.stringify(dataToPost),
          dataType: 'json',
          contentType: 'application/json',
          success: function(data){
            alert('ok');
            console.log(data);
          },
          error: function(xhr, type){
            console.log('无法连接服务器');
          }
        });
      }
    },
    watch: {
      immType(){
        /**
         * 从ImmType解析出机器类型，是否大机，是否双注射
         * @type {string[]}
         */
        this.isBigImm = false;
        this.isDualInj = false;
        this.clampForce = 0;
        this.injection = 0;
        this.type = '';
        if(this.immType === ''){
          console.log('_parseImmType失败，immType为空字符串');
          return;
        }
        // 去除this.immType开头和末尾的空格
        this.immType = this.immType.replace(/^\s+/, '');
        this.immType = this.immType.replace(/\s+$/, '');
        let temp = this.immType.split(/[-/\s]/);
        if(temp.length !== 2){
          console.log("切分锁模力与注射量时出错：this.immType格式问题，'/'或'-'或' '是分隔锁模力与注射量的敏感字符，必须只能出现1次");
          alert("机型格式有误，错误信息见控制台信息");
          return;
        }
        let substr1 = temp[0].toUpperCase();
        let substr2 = temp[1];
        // 我觉得目前锁模力都是两位数起步，这里匹配10kn及以上的锁模力，同时防止出现类似VE2S80这种干扰。
        temp = substr1.match(/\d{2,}/);
        if(!temp){
          console.log("解析锁模力时出错：this.immType格式问题，参考格式'ZE1200s/300'");
          alert("机型格式有误，错误信息见控制台信息");
          return;
        }
        this.clampForce = temp[0];
        // 判断是否是ZEs ZE VE2s VE2等4中机型
        if(substr1.indexOf('ZE') > -1){
          if(substr1.indexOf('S') > -1){
            this.type = 'ZEs';
          }else{
            this.type = 'ZE';
          }
        }else if(substr1.indexOf('VE') > -1){
          if(substr1.indexOf('S') > -1){
            this.type = 'VE2s';
          }else{
            this.type = 'VE2';
          }
        }else{
          console.log("机械机型时出错：this.immType格式问题，该字符串没有包含'ze'或've'关键字");
          alert("机型格式有误，错误信息见控制台信息");
          return;
        }
        this.injection = substr2.replace(/[^0-9]+/, '');
        // 判断是否大机以及单双注射
        if(this.clampForce >= 4500){
          this.isBigImm = true;
        }
        if(this.type === 'ZE' || this.type === 'VE2'){
          if(this.injection >= 2250){
            this.isDualInj = true;
          }
        }else{
          if(this.injection >= 1400){
            this.isDualInj = true;
          }
        }
      }
    }
  }
</script>
<style lang="scss" scoped>
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
  .vanish-left-enter-active, .vanish-left-leave-active{
    transition: all .5s ease;
  }
  .vanish-left-enter, .vanish-left-leave-to{
    opacity: 0;
    margin-left: -66.7%
  }
  .vanish-right-enter-active, .vanish-right-leave-active{
    transition: all .5s ease;
  }
  .vanish-right-enter, .vanish-right-leave-to{
    opacity: 0;
    margin-right: -66.7%;
  }
  footer{
    background-color: #eee;
    display: flex;
    justify-content: center;
    i{
      color: #ccc;
      cursor: pointer;
    }
    a{
      margin:{
        left: 50px;
        right: 50px;
      }
      text-decoration: none;
      color: #ccc;
    }
    .enable{
      transition: all .5s;
      &:hover{
        color: black;
      }
    }
  }
</style>
