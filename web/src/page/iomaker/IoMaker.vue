<template>
    <div id="iomaker" v-loading="waiting">
      <div class="container-fluid">
        <!-- 信息录入 & 功能配置 -->
        <div class="row" v-show="curStep === 1">
          <div class="col-sm-4 wrapper">
            <info-form
              :getInfo="getInfo"
              @imminfochange="getImmInfo">
            </info-form>
          </div>
          <div class="col-sm-8 wrapper">
            <func-config
              :type="type"
              :funcOutputItems="funcOutputItems"
              @functionsupdate="getFuncConfig"
              @exthotrunnerchange="getExtHotrunnerNum"
              @inthotrunnerchange="getIntHotrunnerNum"
              @funcoutput1change="getFuncOutput1"
              @funcoutput2change="getFuncOutput2"
            />
          </div>
        </div>
        <!-- IO选择区域 & IO硬件配置区 -->
        <div class="row" v-show="curStep === 2">
          <div class="col-sm-5 wrapper">
            <io-list
              :allIO="allIO"
              :loading="!ajaxIOLoadOK"
              :usedIO="usedIO"
              @newioappend="getNewIoAppend"
            />
          </div>
          <div class="col-sm-7 wrapper hardware-area">
            <hardware-title
              :type="type"
              :mainBoardSlots="mainBoardSlots"
              :extendBoard1Slots="extendBoard1Slots"
              :extendBoard2Slots="extendBoard2Slots"
              @moduleselectupdate="getHardwareTitleInfo"
            />
            <hardware-module
              :moduleName="curModuleName"
              :ioConfig="curModuleIoConfig"
              :allIO="allIO"
              :ioInfoLoaded="ajaxIOLoadOK"
              :curBoard="curHardwareTitleIdx"
              :newIoToAppend="newIoToAppend"
              v-if="curHardwareTitleIdx > 1"
              @moduleiosupdate="getHardwareModuleIoInfo"
              @varanposupdate="getVaranConnModulePosInfo"
            />
            <std-io
              v-else
              :ioType="curStdIoType"
              :stdIo="stdIo"
              :originStdIo="originStdIo"
              :loading="!ajaxIOLoadOK"
              :allIO="allIO"
              @stdioupdate="getConfiguredStdIoInfo"
            />
          </div>
        </div>
      </div>
      <!-- 左右滑动页面按钮 -->
      <page-switch direction="left" v-show="curStep === 2" @click.native="slidePrev"/>
      <page-switch direction="right" v-show="curStep === 1" @click.native="slideNext"/>
      <!-- 页脚信息提交栏 -->
      <footer class="fixed-bottom">
        <i class="fa fa-angle-left fa-3x to-left" :class="{'enable': curStep !== 1}" aria-hidden="true" @click="slidePrev"></i>
        <div>
          <a href="#checkInfoBeforeSubmit" class="fa-2x enable" @click="popModalIO" data-toggle="modal">IO表</a>
        </div>
        <div>
          <a href="#checkInfoBeforeSubmit" class="fa-2x enable" @click="popModalConfig" data-toggle="modal">配置文件</a>
        </div>
        <div>
          <a href="#" class="fa-2x enable" @click="resetAllInfo" data-toggle="modal">重置</a>
        </div>
        <i class="fa fa-angle-right fa-3x to-right" :class="{'enable': curStep !== 2}" aria-hidden="true" @click="slideNext"></i>
      </footer>
      <!-- 配置信息确认模态框 -->
      <div class="modal fade" id="checkInfoBeforeSubmit" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLongTitle">
                <span v-if="modalType===0">即将创建IO表</span>
                <span v-if="modalType===1">即将创建配置文件</span>
              </h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              机型：{{type}}&nbsp;{{clampForce}}-{{injection}}<br>
              <div v-if="ceStandard && modalType===1" class="font-weight-bold text-danger">
                <span>&nbsp;&nbsp;CE</span>
                <div class="btn-group dropright">
                  <i class="fa fa-cog text-danger pointer" aria-hidden="true" aria-haspopup="true" aria-expanded="false"
                     data-toggle="dropdown"
                     :class="{'fa-spin': pilzNor===''}">
                  </i>
                  <div class="dropdown-menu">
                    <a href="#" v-for="item in pilzList['normal']" @click="pilzNor=item" class="dropdown-item">{{item}}</a>
                  </div>
                </div>
                <span class="pl-5">{{pilzNor}}</span>
                <span v-show="pilzNor===''" class="float-right"><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>请选择安全继电器文件</span>
              </div>
              <div v-if="ceStandard && modalType===0" class="font-weight-bold text-danger">
                <span>&nbsp;&nbsp;CE</span>
              </div>
              <div v-if="funcConfig[3].status && modalType===1" class="font-weight-bold text-danger">
                <span>E73</span>
                <div class="btn-group dropright">
                  <i class="fa fa-cog text-danger pointer" aria-hidden="true" aria-haspopup="true" aria-expanded="false"
                     data-toggle="dropdown"
                     :class="{'fa-spin': pilzE73===''}"></i>
                  <div class="dropdown-menu">
                    <a href="#" v-for="item in pilzList['e73']" @click="pilzE73=item" class="dropdown-item">{{item}}</a>
                  </div>
                </div>
                <span class="pl-5">{{pilzE73}}</span>
                <span v-show="pilzE73===''" class="float-right"><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>请选择E73文件</span>
              </div>
              <div v-if="funcConfig[3].status && modalType===0" class="font-weight-bold text-danger">
                <span>E73</span>
              </div>
              <hr>
              主底板模块: {{mainBoardSlots}}<br>
              <hr>
              扩展底板一：{{extendBoard1Slots}}<br>
              <hr>
              扩展底板二：{{extendBoard2Slots}}<br>
              <hr>
              能耗模块：<span class="font-weight-bold" :class="{'text-danger': funcConfig[5].status}">{{funcConfig[5].status}}</span>
              <hr>
              外置热流道：<span class="font-weight-bold" :class="{'text-danger': funcConfig[99].status}">{{funcConfig[99].status}}</span>
              <div v-show="funcConfig[99].status">{{extHotrunnerNum}}</div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
              <button type="button" class="btn btn-primary" @click="submitInfo">提交</button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  import IoList from './components/IoList'
  import InfoForm from './components/InfoForm'
  import FuncConfig from './components/FuncConfig'
  import HardwareTitle from './components/HardwareTitle'
  import HardwareModule from './components/HardwareModule'
  import StdIo from './components/StdIo'
  import PageSwitch from './components/PageSwitch'
  import axios from 'axios'

  // 标准中没有“第八段加热”，为了方便配置CAI888，特新增16号AI点：“第八段加热”
  const CAI888_IO_CONFIG = {'TI1': 1, 'TI2': 2, 'TI3': 3, 'TI4': 4, 'TI5': 5, 'TI6': 6, 'TI7': 7, 'TI8': 16,
  'TO1': 1, 'TO2': 2, 'TO3': 3, 'TO4': 4, 'TO5': 5, 'TO6': 6, 'TO7': 7, 'TO8': 8};

  export default {
    name: 'IoMaker',
    components:{
      IoList,
      InfoForm,
      FuncConfig,
      HardwareTitle,
      HardwareModule,
      StdIo,
      PageSwitch,
    },
    data(){
      return{
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
          3: {name: 'E73', status: false},
          5: {name: 'DEE能耗模块', status: false},
          98: {name: 'PSG热流道', status: false},
          99: {name: '外置热流道', status: false},
          101: {name: '阀门', status: false},
          102: {name: '吹气', status: false},
          103: {name: '中子', status: false},
          104: {name: '可编程IO', status: false}
        },
        extHotrunnerNum: 3,
        intHotrunnerNum: 0,
        funcOutput1: 0,
        funcOutput2: 0,
        // 解析immType后得到的数据
        isBigImm: false,
        isDualInj: false,
        clampForce: 0,
        injection: 0,
        type: '',
        ceStandard: false,
        // 安全继电器信息
        pilzList: {'normal': ['获取文件失败'], 'e73': ['获取文件失败']},
        pilzNor: '',
        pilzE73: '',

        // 控制页面的展示内容：信息录入 或 IO选配（左右移动）
        curStep: 1,
        // 从InfoForm获取immInfo的标志位，通过prop传递到InfoForm组件，
        // InfoForm检测到该值为true时，触发imminfochange事件
        getInfo: false,
        // 从IoList组件鼠标双击获取过来的IO，将由Module组件获取该IO信息并添加到当前模块的按顺序排列的可用空余点位
        // 正常情况下，该值应该为 ''
        newIoToAppend: '',
        // POST后等待后台返回数据
        waiting: false,
        // 控制弹出modal的样式， 0：IO     1: 配置文件
        modalType: 0,
        // 功能点1和2可配置的选项
        funcOutputItems: [],
        // 所有的IO点，格式为{'DI': ['开门止', 'xxx', ...], 'DO': ['xx', ...], ...}
        allIO: {'DI': [], 'DO': [], 'AI': [], 'AO': [], 'TI': [], 'TO': []},
        ajaxIOLoadOK: false,
        // 底板/模块系统IO点位配置, 格式为{ 'DI': [9, 10 ,..., 0, 17], 'DO': [], ...}
        // 其中数组元素依次代表某个位置配置的IO序号，0表示未配置
        stdIo: {'DI': [], 'DO': [], 'AI': [], 'AO': [], 'TI': [], 'TO': []},
        // ajax获取到的标准底板/模块系统IO点，格式与stdIo一致
        originStdIo: {'DI': [], 'DO': [], 'AI': [], 'AO': [], 'TI': [], 'TO': []},
        // HardwareTitle
        curHardwareTitleIdx: 1,
        curHardwareSlotIdx: 1,
        mainBoardSlots: ['', '', '', ''],
        extendBoard1Slots: ['', '', '', ''],
        extendBoard2Slots: ['', '', '', ''],
        // HardwareIO
        mainBoardModuleIos: [{}, {}, {}, {}],
        extendBoard1ModulesIos: [{}, {}, {}, {}],
        extendBoard2ModulesIos: [{}, {}, {}, {}],
        // Varan连接模块安装位置，0代表在KEB之后，1代表在KEB之前
        varanConnModulePos: 0,
      }
    },
    computed: {
      curModuleName () {
        let name = '';
        switch (this.curHardwareTitleIdx) {
          case 1:
            name = this.mainBoardSlots[0];
            break;
          case 2:
            name = this.mainBoardSlots[this.curHardwareSlotIdx - 1];
            break;
          case 3:
            name = this.extendBoard1Slots[this.curHardwareSlotIdx - 1];
            break;
          case 4:
            name = this.extendBoard2Slots[this.curHardwareSlotIdx - 1];
            break;
        }
        return name;
      },
      curModuleIoConfig () {
        let ioConfig = {};
        switch (this.curHardwareTitleIdx) {
          case 1:
            ioConfig = this.mainBoardModuleIos[0];
            break;
          case 2:
            ioConfig = this.mainBoardModuleIos[this.curHardwareSlotIdx - 1];
            break;
          case 3:
            ioConfig = this.extendBoard1ModulesIos[this.curHardwareSlotIdx - 1];
            break;
          case 4:
            ioConfig = this.extendBoard2ModulesIos[this.curHardwareSlotIdx - 1];
            break;
        }
        return ioConfig;
      },
      curStdIoType () {
        let ioType = '';
        if (this.curHardwareTitleIdx === 1) {
          switch (this.curHardwareSlotIdx) {
            case 1:
              ioType = 'DI';
              break;
            case 2:
              ioType = "DO";
              break;
            case 3:
              ioType = 'AI';
              break;
            case 4:
              ioType = 'AO';
              break;
            case 5:
              ioType = 'TI';
              break;
            case 6:
              ioType = 'TO';
              break;
          }
        }
        return ioType;
      },
      usedIO () {
        let _usedIo = {'DI': [], 'DO': [], 'AI': [], 'AO': [], 'TI': [], 'TO': []};
        if (!this.ajaxIOLoadOK) {
          return _usedIo;
        }
        for (let ioType in this.stdIo) {
          // 计入底板上已使用的IO点
          for (let item of this.stdIo[ioType]) {
            if (item != 0) {
              _usedIo[ioType].push(item);
            }
          }
        }
        for (let module of this.mainBoardModuleIos) {
          for (let key in module) {
            let ioType = key.slice(0, 2);
            _usedIo[ioType].push(module[key]);
          }
        }
        for (let module of this.extendBoard1ModulesIos) {
          for (let key in module) {
            let ioType = key.slice(0, 2);
            _usedIo[ioType].push(module[key]);
          }
        }
        for (let module of this.extendBoard2ModulesIos) {
          for (let key in module) {
            let ioType = key.slice(0, 2);
            _usedIo[ioType].push(module[key]);
          }
        }
        return _usedIo;
      },
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
      getFuncConfig(e){
        this.funcConfig = e;
        if(!this.funcConfig[3].status){
          this.pilzE73 = ''
        }
      },
      getExtHotrunnerNum(e){
        this.extHotrunnerNum = e;
      },
      getIntHotrunnerNum(e){
        this.intHotrunnerNum = e;
      },
      getFuncOutput1 (e) {
        this.funcOutput1 = e;
      },
      getFuncOutput2 (e) {
        this.funcOutput2 = e;
      },
      getNewIoAppend(e){
        this.newIoToAppend = e;
      },
      submitInfo(){
        if(this.modalType === 1){
          if(this.ceStandard && this.pilzNor === ''){
            this.$message({
              message: '请选择安全继电器文件',
              type: 'warning'
            });
            return;
          }
          if(this.funcConfig[3].status && this.pilzE73 === ''){
            this.$message({
              message: '请选择E73文件',
              type: 'warning'
            });
            return;
          }
        }
        let dataToPost = {
          boardModules1: this.mainBoardSlots,
          boardModules2: this.extendBoard1Slots,
          boardModules3: this.extendBoard2Slots,
          boardModulesIOs1: this.mainBoardModuleIos,
          boardModulesIOs2: this.extendBoard1ModulesIos,
          boardModulesIOs3: this.extendBoard2ModulesIos,
          varanConnModulePos: this.varanConnModulePos,
          evaluationNum: this.evaluationNum,
          productionNum: this.productionNum,
          immType: this.immType,
          customer: this.customer,
          safetyStandard: this.safetyStandard,
          technicalClause: this.technicalClause,
          designNote: this.designNote,
          funcConfig: this.funcConfig,
          funcOutput1: this.funcOutput1,
          funcOutput2: this.funcOutput2,
          pilzNor: this.pilzNor,
          pilzE73: this.pilzE73,
          extHotrunnerNum: this.extHotrunnerNum,
          intHotrunnerNum: this.intHotrunnerNum,
          isBigImm: this.isBigImm,
          isDualInj: this.isDualInj,
          clampForce: this.clampForce,
          injection: this.injection,
          type: this.type,
          ceStandard: this.ceStandard,
          mainBoardModifiedIo: this.getMainBoardModifiedIo(),
        };
        let _this = this;
        let url;
        if(this.modalType === 0){
          url = '/api/io/createxlxs';
        }
        if(this.modalType === 1){
          url = '/api/io/createconfigfile';
        }
        $.ajax({
          type: 'POST',
          url: url,
          data: JSON.stringify(dataToPost),
          dataType: 'json',
          contentType: 'application/json',
          beforeSend: function () {
            _this.waiting = true;
          },
          success: function (data) {
            _this.waiting = false;
            // 下载文件
            if (data.status.toUpperCase() === 'SUCCESS' && data.url) {
              window.open(data.url);
            }else{
              alert('后台遇到错误，无法生成文件，错误描述：' + data.description);
            }
          },
          error: function (xhr, type) {
            _this.waiting = false;
            alert('无法连接服务器');
          }
        });
        $('#checkInfoBeforeSubmit').modal('hide');
      },
      slideNext(){
        this.curStep = 2;
        this.getInfo = true;
      },
      slidePrev(){
        this.curStep = 1;
      },
      getVaranConnModulePosInfo(e){
        this.varanConnModulePos = e;
      },
      resetAllInfo(){
        if(confirm('清空所有配置信息？')){
          // location.reload();
          this.$router.go(0);
        }
      },
      popModalIO(){
        this.getInfo = true;
        this.modalType = 0;
      },
      popModalConfig(){
        this.getInfo = true;
        this.modalType = 1;
      },
      getHardwareTitleInfo (e) {
        this.curHardwareTitleIdx = e.curTitleIdx;
        this.curHardwareSlotIdx = e.curSlotIdx;
        switch (e.curTitleIdx) {
          case 2:
            for (let i=0; i<this.mainBoardSlots.length; i++) {
              if (this.mainBoardSlots[i] !== e.slots[i]) {
                this.$set(this.mainBoardSlots, i, e.slots[i]);
                if (e.slots[i] === 'CAI888') {
                  this.$set(this.mainBoardModuleIos, i, CAI888_IO_CONFIG);
                } else {
                  this.$set(this.mainBoardModuleIos, i, {});
                }
              }
            }
            break;
          case 3:
            for (let i=0; i<this.extendBoard1Slots.length; i++) {
              if (this.extendBoard1Slots[i] !== e.slots[i]) {
                this.$set(this.extendBoard1Slots, i, e.slots[i]);
                if (e.slots[i] === 'CAI888') {
                  this.$set(this.extendBoard1ModulesIos, i, CAI888_IO_CONFIG);
                } else {
                  this.$set(this.extendBoard1ModulesIos, i, {});
                }
              }
            }
            break;
          case 4:
            for (let i=0; i<this.extendBoard2Slots.length; i++) {
              if (this.extendBoard2Slots[i] !== e.slots[i]) {
                this.$set(this.extendBoard2Slots, i, e.slots[i]);
                if (e.slots[i] === 'CAI888') {
                  this.$set(this.extendBoard2ModulesIos, i, CAI888_IO_CONFIG);
                } else {
                  this.$set(this.extendBoard2ModulesIos, i, {});
                }
              }
            }
            break;
        }
      },
      getHardwareModuleIoInfo (e) {
        switch (this.curHardwareTitleIdx) {
          case 1:
            alert('当前主底板页面不应出现模块IO刷新啊,js代码出现了严重问题');
            break;
          case 2:
            this.$set(this.mainBoardModuleIos, this.curHardwareSlotIdx - 1, e);
            break;
          case 3:
            this.$set(this.extendBoard1ModulesIos, this.curHardwareSlotIdx - 1, e);
            break;
          case 4:
            this.$set(this.extendBoard2ModulesIos, this.curHardwareSlotIdx - 1, e);
            break;
        }
        this.newIoToAppend = '';
      },
      getBigImmStdIo () {
        let bigImmModule = 'CIO021';
        let cio0x1Ios = {
          'DI3': 83,
          'DI4': 84,
          'DI5': 85,
          'DI6': 97,
          'DI7': 98,
          'DI8': 99,
          'DO1': 97,
          'DO2': 98,
          'DO3': 113
        };
        if (this.type === 'VE2') {
          bigImmModule = 'CIO011';
        }
        this.$set(this.mainBoardSlots, 0, bigImmModule);
        this.$set(this.mainBoardModuleIos, 0, cio0x1Ios);

        if (this.type === 'ZEs' || this.type === 'ZE') {
          this.$set(this.stdIo['DI'], 16, 102);
          this.$set(this.stdIo['DI'], 17, 95);
        }
      },
      resetNotBigImmStdIo () {
        this.$set(this.mainBoardSlots, 0, '');
        if (this.type === 'ZEs' || this.type === 'ZE') {
          this.$set(this.stdIo['DI'], 16, 0);
          this.$set(this.stdIo['DI'], 17, 0);
        }
      },
      getConfiguredStdIoInfo (e) {
        this.stdIo[this.curStdIoType] = e;
      },
      getMainBoardModifiedIo () {
        // 返回格式: {'DI7': 23, 'DO36': 0, ...}
        let mainBoardModifiedIo = {};

        for (let ioType in this.stdIo) {
          for (let i=0; i<this.stdIo[ioType].length; i++) {
            if (this.stdIo[ioType][i] !== this.originStdIo[ioType][i]) {
              mainBoardModifiedIo[ioType + (i + 1)] = this.stdIo[ioType][i];
            }
          }
        }
        return mainBoardModifiedIo;
      },
      getStdIo () {
        axios.get("/api/io/stdio", {
          params: {
            type: this.type,
            ceStandard: this.ceStandard
          }
        }).then(res => {
          this.stdIo = res.data.stdIo;
          this.originStdIo = JSON.parse(JSON.stringify(this.stdIo));
        }).catch ( e => {
          console.log(e);
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
          if(substr1.indexOf('S') > -1 || substr1.includes('Ⅲ') || substr1.includes('III')){
            this.type = 'ZEs';
          }else{
            this.type = 'ZE';
          }
        }else if(substr1.indexOf('VE') > -1){
          if(substr1.indexOf('S') > -1 || substr1.includes('Ⅲ') || substr1.includes('III')){
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
      },
      safetyStandard(){
        this.ceStandard = true;
        if(this.safetyStandard.search(/亚洲|非CE|无CE|not|国标/i) > -1) {
          this.ceStandard = false;
          this.pilzNor = '';
        }
        if(this.safetyStandard === ''){
          this.ceStandard = false;
          this.pilzNor = '';
        }
      },
      isBigImm () {
        if (this.isBigImm) {
          this.getBigImmStdIo();
        } else {
          this.resetNotBigImmStdIo();
        }
      },
      type () {
        this.getStdIo();
        if (this.isBigImm) {
          this.getBigImmStdIo();
        }
      },
      ceStandard () {
        this.getStdIo();
        if (this.isBigImm) {
          this.getBigImmStdIo();
        }
      }
    },
    mounted(){
      let _this = this;
      $.ajax({
        url: "/api/io/pilzlist",
        type: 'GET',
        dataType: 'json',
        success: function(data){
          _this.pilzList = data;
        },
        error: function(){
          console.log('AJAX请求失败，无法获取Pilz文件列表');
        }
      });
      // 获取功能点1和2可配置选项
      axios.get('/api/io/funcoutlist').then( (res) => {
        this.funcOutputItems = res.data;
      }).catch( (e)=> {
        console.log(e);
        this.funcOutputItems = [
          '关闭',
          '注射开始',
          '储料开始',
          '可编程输出1',
          '可编程输出2',
          '包装箱满',
          '吹气5',
          '吹气6',
          '液压回油阀(特殊)'
        ];
      });
      axios.get('/api/io/allio').then( res => {
        this.allIO = res.data;
        this.ajaxIOLoadOK = true;
      }).catch( e => {
        console.log(e);
      });
    }
  }
</script>
<style lang="scss" scoped>
  footer{
    background-color: #eee;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    opacity: .8;
    i{
      color: #ccc;
      cursor: pointer;
      flex: 1;
      &.to-left {
        text-align: left;
      }
      &.to-right {
        text-align: right;
      }
    }
    a{
      margin:{
        left: 40px;
        right: 40px;
      }
      text-decoration: none;
      color: #ccc;
      outline: none;
    }
    .enable{
      transition: color .5s;
      &:hover{
        color: black;
      }
    }
  }
  .pointer{
    cursor: pointer;
  }
  #srcmaker{
    /* 防止底部被footer遮挡 */
    padding-bottom: 3rem;
  }
  .container-fluid {
    position: absolute;
    top: 56px;
    bottom: 48px;
    left: 0;
    right: 0;
    .row {
      height: 100%;
    }
  }
  .wrapper {
    height: 100%;
  }
  .hardware-area {
    overflow: auto;
    box-sizing: border-box;
    &::-webkit-scrollbar{
      height: 6px;
      width: 6px;
    }
    &::-webkit-scrollbar-thumb{
      border-radius: 10px;
      -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
      background: #818080;
    }
  }
</style>
