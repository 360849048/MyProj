<template>
    <div id="srcmaker" v-loading="waiting">
      <div class="container-fluid">
        <div class="row">
          <!-- 信息录入 -->
          <transition name="fade-left">
            <div class="col-sm-4" v-show="curStep === 1">
              <info-form
                :getInfo="getInfo"
                @imminfochange="getImmInfo">
              </info-form>
            </div>
          </transition>
          <!-- 功能配置 -->
          <transition name="vanish-left">
            <div class="col-sm-8" v-show="curStep === 1">
              <func-config
              @functionsupdate="getFuncConfig">
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
                :boardModulesIOs3="boardModulesIOs3"
                @newioappend="getNewIoAppend">
              </io-list>
            </div>
          </transition>
          <!-- 模块显示区 -->
          <transition name="fade-right">
            <div class="col-sm-4" id="module_area" v-show="curStep === 2" >
              <module
                :big-imm="isBigImm"
                :type="type"
                :new-io-to-append="newIoToAppend"
                @modulesupdate="getModuleInfo">
              </module>
            </div>
          </transition>
        </div>
      </div>
      <div id="slidePrev" v-show="curStep === 2" @click="slidePrev">
        <i class="fa fa-angle-left fa-3x"></i>
      </div>
      <div id="slideNext" v-show="curStep === 1" @click="slideNext">
        <i class="fa fa-angle-right fa-3x"></i>
      </div>
      <footer class="fixed-bottom">
        <i class="fa fa-angle-left fa-3x" :class="{'enable': curStep !== 1}" aria-hidden="true" @click="slidePrev"></i>
        <div id="postInfo">
          <a href="#exampleModalLong" class="fa-2x enable" @click="getInfo=true" data-toggle="modal">提交</a>
        </div>
        <i class="fa fa-angle-right fa-3x" :class="{'enable': curStep !== 2}" aria-hidden="true" @click="slideNext"></i>
      </footer>
      <!-- 配置信息确认模态框 -->
      <div class="modal fade" id="exampleModalLong" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLongTitle">请确认配置信息</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              机型：{{immType}}<br>
              安全：{{safetyStandard}}
              <hr>
              主底板模块: {{boardModules1}}<br>
              IO: {{boardModulesIOs1}}
              <hr>
              扩展底板一：{{boardModules2}}<br>
              IO: {{boardModulesIOs2}}
              <hr>
              扩展底板二：{{boardModules3}}<br>
              IO: {{boardModulesIOs3}}
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="submitInfo">确认提交</button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  /**
   * 数据处理逻辑：
   * 1.从infoForm收集机器基础信息，并根据immType解析机器具体参数信息：机器类型、单双注射、大机选配
   *   为了避免频繁触发imminfochange事件，通过设置this.getInfo=true可以从FuncForm读取一次信息
   * 2.从FuncForm获取主底板IO修改信息：功能点12的配置等信息。
   *  TODO:功能配置文件信息录入
   * 3.从Module获取模块和模块上的IO配置信息，并将配置信息传递到IoList组件
   * 4.页脚处放置的一些按钮，用来移动展示页面以及向后台POST机器信息
   * 5.IoList接受HTML5的drag事件，ModuleConfig接受HTML5的drop事件，通过鼠标拖拽的方法可实现模块点位的配置
   * 6.TODO: 在IoList的IO列表上某项双击，自动将该IO填充到模块的最靠前空余的IO点上
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
        // 机器功能配置信息，包括主底板默认IO修改信息
        funcConfig: {
          1: {name: '功能点1注射信号', status: false},
          2: {name: '功能点2储料信号', status: false},
          3: {name: 'E73', status: false},
          4: {name: '喷嘴改阀门1', status: false}
        },
        // 解析immType后得到的数据
        isBigImm: false,
        isDualInj: false,
        clampForce: 0,
        injection: 0,
        type: '',

        // 控制页面的展示内容：信息录入 或 IO选配（左右移动）
        curStep: 1,
        // 从InfoForm获取immInfo的标志位，通过prop传递到InfoForm组件，
        // InfoForm检测到该值为true时，触发imminfochange事件
        getInfo: false,
        // 从IoList组件鼠标双击获取过来的IO，将由Module组件获取该IO信息并添加到当前模块的按顺序排列的可用空余点位
        // 正常情况下，该值应该为 ''
        newIoToAppend: '',
        // POST后等待后台返回数据
        waiting: false
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
        // 清除获取信息标志位
        this.getInfo = false;
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

        // 及时清空新加IO信息，防止重复添加该IO
        this.newIoToAppend = '';
      },
      getFuncConfig(e){
        this.funcConfig = e;
      },
      getNewIoAppend(e){
        this.newIoToAppend = e;
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
          funcConfig: this.funcConfig,
          isBigImm: this.isBigImm,
          isDualInj: this.isDualInj,
          clampForce: this.clampForce,
          injection: this.injection,
          type: this.type
        };
        let _this = this;
        $.ajax({
          type: 'POST',
          url: '/iomaker',
          data: JSON.stringify(dataToPost),
          dataType: 'json',
          contentType: 'application/json',
          beforeSend: function(){
            _this.waiting = true;
          },
          success: function(data){
            _this.waiting = false;
            // 下载文件
            if(data.ioFileUrl){
              window.open(data.ioFileUrl);
            }
          },
          error: function(xhr, type){
            _this.waiting = false;
            alert('无法连接服务器');
          }
        });
      },
      slideNext(){
        this.curStep = 2;
        this.getInfo = true;
      },
      slidePrev(){
        this.curStep = 1;
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
  #slidePrev, #slideNext{
    $height: 25rem;
    position: absolute;
    top: 50%;
    transform: translateY(- ($height / 2));
    width: 3rem;
    height: $height;
    background-color: #ccc;
    opacity: 0.2;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all .2s;
  }
  #slidePrev{
    left: -2.5rem;
    border-radius: 0 20px 20px 0;
    &:hover{
      opacity: .5;
      left: 0;
      cursor: pointer;
    }
  }
  #slideNext{
    right: -2.5rem;
    border-radius: 20px 0 0 20px;
    &:hover{
      opacity: .5;
      right: 0;
      cursor: pointer;
    }
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
      outline: none;
    }
    .enable{
      transition: all .5s;
      &:hover{
        color: black;
      }
    }
  }
</style>
