<template>
  <div id="module">
    <ul id="DI" class="io-module">
      <li class="io-line" v-for="(item, index) in mDI" :key="index" v-if="index <= mDiAmount"
          :data-index="index" data-type="di"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-success io-index">DI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item" @dblclick="dblclickIO">
          {{item | nameOnly}}
        </div>
      </li>
    </ul>
    <ul id="DO" class="io-module">
      <li class="io-line" v-for="(item, index) in mDO" :key="index" v-if="index <= mDoAmount"
          :data-index="index" data-type="do"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-danger io-index">DO&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item" @dblclick="dblclickIO">
          {{item | nameOnly}}
        </div>
      </li>
    </ul>
    <ul id="AI" class="io-module">
      <li class="io-line" v-for="(item, index) in mAI" :key="index" v-if="index <= mAiAmount"
          :data-index="index" data-type="ai"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-info io-index">AI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item" @dblclick="dblclickIO">
          {{item | nameOnly}}
        </div>
      </li>
    </ul>
    <ul id="AO" class="io-module">
      <li class="io-line" v-for="(item, index) in mAO" :key="index" v-if="index <= mAoAmount"
          :data-index="index" data-type="ao"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-warning io-index">AO&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item" @dblclick="dblclickIO">
          {{item | nameOnly}}
        </div>
      </li>
    </ul>
    <ul id="TI" class="io-module">
      <li class="io-line" v-for="(item, index) in mTI" :key="index" v-if="index <= mTiAmount"
          :data-index="index" data-type="ti"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-info io-index">TI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item" @dblclick="dblclickIO">
          {{item | nameOnly}}
        </div>
      </li>
    </ul>
    <ul id="TO" class="io-module">
      <li class="io-line" v-for="(item, index) in mTO" :key="index" v-if="index <= mToAmount"
          :data-index="index" data-type="to"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-warning io-index">TO&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item" @dblclick="dblclickIO">
          {{item | nameOnly}}
        </div>
      </li>
    </ul>
    <!-- 单独处理CIV512等连接模块 -->
    <div v-if="moduleName.toUpperCase() === 'CIV512' || moduleName.toUpperCase() === 'CIV521'">
      <p class="h1">
        您已激活扩展该底板，连接模块是：{{moduleName}}
      </p>
      <div v-show="curBoard == 2">
        <hr>
        <p class="h5">{{moduleName}}位置选择</p>
        <div class="custom-control custom-radio">
          <input type="radio" id="beforeKeb" name='varanPosSet' class="custom-control-input" value="0" v-model="varanConnModulePos">
          <label class="custom-control-label" for="beforeKeb">KEB之后</label>
        </div>
        <div class="custom-control custom-radio">
          <input type="radio" id="afterKeb" name='varanPosSet' class="custom-control-input" value="1" v-model="varanConnModulePos">
          <label class="custom-control-label" for="afterKeb">KEB之前</label>
        </div>
      </div>
      <div v-show="curBoard == 3">
        <hr>
        <i class="fa fa-exclamation text-danger" aria-hidden="true"></i>
        <span>底板三功能尚未开发完全，无法写入IO表和硬件配置</span>
      </div>

    </div>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 1.检测到props属性moduleName变化时：
   *  初始化模块IO点（调用_initModuleIO依次初始化mDiAmount,mDoAmount,mAiAmount,mAoAmount,mDI,mDO,mAI,mAO）。
   * 2.检测到props属性ios变化时：
   *  先根据moduleName，初始化模块IO点。然后读取ios的信息，写入到mDI,mDO,mAI,mAO。
   * 3.响应HTML5的drop事件：
   *  解析drag--drop传递过来的信息，更新mDI,mDO,mAI,mAO。然后触发moduleiosupdate事件，向父组件发送当前模块的IO信息。
   *  TODO: 通过dragover反馈，改善使用体验
   * 4.响应IO点上的dblclick事件：
   *  根据当前模块点的Index，对mDI或mDO或mAI或mAO的相应点进行写入空值''。然后触发moduleiosupdate事件，向父组件发送当前模块的IO信息。
   * 5.moduleiosupdate事件传递一个json格式如下:
   *    {
   *       do1: 43--阀门1开,
   *       di3: 73--可编程IO输入1,
   *       ...
   *    }
   * 6.接收父组件newIoToAppend，watch该变量变动，并触发moduleioupdate事件
   * 7.varanposupdate事件传递CIV512等Varan连接模块的安装位置信息。0：KEB之后； 1：KEB之前
   *
   * 注意：只有在“具体”节点发生drop和dblclick事件，该模块才会触发父组件修改IO信息。
   */
    export default {
      name: "module-config",
      props: [
        // 接收父组件传递过来的字符串，
        // 例如："CDM613"
        'moduleName',
        // 接收从父组件传递过来的json对象，用来配置点位
        // 例如: {'do1': 43--阀门1开, 'di2': 73--可编程IO输出1}
        'ios',
        // 从IoList鼠标双击触发传递过来的IO信息
        'newIoToAppend',
        // 当前活动的底板
        'curBoard'
      ],
      data(){
        return{
          // 当 XX[?] === undefined  时，该模块只拥有(?-1)个此类型的IO点。
          // 比如 mDI[1] === undefined, 说明该模块没有DI点。
          // 再如 mDI[9] === undefined,说明该模块只有8个DI点。
          mDI: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''},
          mDO: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''},
          mAI: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''},
          mAO: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''},
          mTI: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''},
          mTO: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''},
          // 以下变量用来统计模块的IO数量
          mDiAmount: 0,
          mDoAmount: 0,
          mAiAmount: 0,
          mAoAmount: 0,
          mTiAmount: 0,
          mToAmount: 0,

          // CIV512或者CIV521这种Varan连接模块的安装位置
          varanConnModulePos: 0
        }
      },
      filters: {
        /**
         * 将数据形式为 "43--阀门1开"，过滤为 "阀门1开"
         */
        nameOnly(value){
          return value.split('--')[1];
        }
      },
      methods: {
        _initModuleIO(moduleName){
          /**
           * 根据当前的模块名，初始化模块信息（清空IO配点信息）
           */
          this.mDI = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''};
          this.mDO = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''};
          this.mAI = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
          this.mAO = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
          this.mTI = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
          this.mTO = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
          this.mDiAmount = 0;
          this.mDoAmount = 0;
          this.mAiAmount = 0;
          this.mAoAmount = 0;
          this.mTiAmount = 0;
          this.mToAmount = 0;
          if(moduleName.toUpperCase() === 'CTO163'){
            this.mDoAmount = 16;
          }
          if(moduleName.toUpperCase() === 'CDM163'){
            this.mDiAmount = 8;
            this.mDoAmount = 8;
          }
          if(moduleName.toUpperCase() === 'CIO021'){
            this.mDiAmount = 8;
            this.mDoAmount = 8;
            this.mAiAmount = 3;
            this.mAoAmount = 2;
          }
          if(moduleName.toUpperCase() === 'CDI163'){
            this.mDiAmount = 16;
          }
          if(moduleName.toUpperCase() === 'CAI888'){
            this.mTiAmount = 8;
            this.mToAmount = 8;
          }
          if(moduleName.toUpperCase() === 'CIO011'){
            this.mDiAmount = 8;
            this.mDoAmount = 8;
            this.mAiAmount = 2;
            this.mAoAmount = 1;
          }
          if(this.mDiAmount < 16){
            this.mDI[this.mDiAmount + 1] = undefined;
          }
          if(this.mDoAmount < 16){
            this.mDO[this.mDoAmount + 1] = undefined;
          }
          if(this.mAiAmount < 16){
            this.mAI[this.mAiAmount + 1] = undefined;
          }
          if(this.mAoAmount < 16){
            this.mAO[this.mAoAmount + 1] = undefined;
          }
          if(this.mTiAmount < 16){
            this.mTI[this.mTiAmount + 1] = undefined;
          }
          if(this.mToAmount < 16){
            this.mTO[this.mToAmount + 1] = undefined;
          }
        },
        _getCurIoConfig(){
          /**
           * 获取当前模块的IO配置信息。
           * 返回数据的格式例如：
           * {do1: 43--阀门1开, ...}
           */
          let ioConfig = {};
          for(let key in this.mDI){
            if(this.mDI[key] === undefined){
              break;
            }
            if(this.mDI[key] !== ''){
              ioConfig['di'+key] = this.mDI[key];
            }
          }
          for(let key in this.mDO){
            if(this.mDO[key] === undefined){
              break;
            }
            if(this.mDO[key] !== ''){
              ioConfig['do'+key] = this.mDO[key];
            }
          }
          for(let key in this.mAI){
            if(this.mAI[key] === undefined){
              break;
            }
            if(this.mAI[key] !== ''){
              ioConfig['ai'+key] = this.mAI[key];
            }
          }
          for(let key in this.mAO){
            if(this.mAO[key] === undefined){
              break;
            }
            if(this.mAO[key] !== ''){
              ioConfig['ao'+key] = this.mAO[key];
            }
          }
          for(let key in this.mTI){
            if(this.mTI[key] === undefined){
              break;
            }
            if(this.mTI[key] !== ''){
              ioConfig['ti'+key] = this.mTI[key];
            }
          }
          for(let key in this.mTO){
            if(this.mTO[key] === undefined){
              break;
            }
            if(this.mTO[key] !== ''){
              ioConfig['to'+key] = this.mTO[key];
            }
          }
          return ioConfig;
        },
        dropIO(e){
          /**
           * 解析drag--drop传递过来的信息，更新mDI,mDO,mAI,mAO。然后触发moduleiosupdate事件，向父组件发送当前模块的IO信息。
           */
          let ioInfo = e.dataTransfer.getData('ioInfo').split('--');
          if(ioInfo.length !== 3){
            console.log(ioInfo, '---数据格式出错');
            return;
          }
          // 解析从父组件拖拽传递过来的数据
          let ioType = ioInfo[0];
          let ioSeq = ioInfo[1];
          let ioName = ioInfo[2];
          // 获取拖拽目的地，必须定位到LI标签
          let dstNode = e.target.tagName === 'LI' ? e.target : e.target.parentNode;
          let thisType = dstNode.getAttribute('data-type');
          if(ioType.toUpperCase() !== thisType.toUpperCase()){
            console.log("类型不一致，无法拖放");
            return;
          }
          let ioIdx = dstNode.getAttribute('data-index');
          if(thisType.toUpperCase() === 'DI'){
            this.mDI[ioIdx] = ioSeq + '--' + ioName;
          }else if(thisType.toUpperCase() === 'DO'){
            this.mDO[ioIdx] = ioSeq + '--' + ioName;
          }else if(thisType.toUpperCase() === 'AI'){
            this.mAI[ioIdx] = ioSeq + '--' + ioName;
          }else if(thisType.toUpperCase() === 'AO'){
            this.mAO[ioIdx] = ioSeq + '--' + ioName;
          }else if(thisType.toUpperCase() === 'TI'){
            this.mTI[ioIdx] = ioSeq + '--' + ioName;
          }else if(thisType.toUpperCase() === 'TO'){
            this.mTO[ioIdx] = ioSeq + '--' + ioName;
          }

          this.$emit('moduleiosupdate', this._getCurIoConfig());
        },
        dblclickIO(e){
          /**
           * 根据当前模块点的Index，对mDI或mDO或mAI或mAO的相应点进行写入空值''。然后触发moduleiosupdate事件，向父组件发送当前模块的IO信息。
           */
          let dstNode = e.target.parentNode;
          let ioIdx = dstNode.getAttribute('data-index');
          let thisType = dstNode.getAttribute('data-type');
          if(ioIdx === null || thisType === null){
            alert("出现了严重错误，打开控制台查看具体错误信息");
            console.log("没有在该节点找到data-index或data-type属性", dstNode);
            return;
          }
          if(thisType.toUpperCase() === 'DI'){
            this.mDI[ioIdx] = '';
          }else if(thisType.toUpperCase() === 'DO'){
            this.mDO[ioIdx] = '';
          }else if(thisType.toUpperCase() === 'AI'){
            this.mAI[ioIdx] = '';
          }else if(thisType.toUpperCase() === 'AO'){
            this.mAO[ioIdx] = '';
          }else if(thisType.toUpperCase() === 'TI'){
            this.mTI[ioIdx] = '';
          }else if(thisType.toUpperCase() === 'TO'){
            this.mTO[ioIdx] = '';
          }
          this.$emit('moduleiosupdate', this._getCurIoConfig());
        }
      },
      watch: {
        moduleName: {
          /**
           * 根据moduleName初始化模块IO点（调用_initModuleIO依次初始化mDiAmount,mDoAmount,mAiAmount,mAoAmount,mDI,mDO,mAI,mAO）
           */
          handler(cval){
            this._initModuleIO(cval);
          },
          deep: false,
          immediate: true,
        },
        ios: {
          /**
           * 先根据moduleName，初始化模块IO点。然后读取ios的信息，写入到mDI,mDO,mAI,mAO,mTI,mTO。
           */
          handler(cval){
            this._initModuleIO(this.moduleName);

            for(let key in cval){
              if (key.toUpperCase().slice(0, 2) === 'DI' ){
                this.mDI[key.slice(2)] = cval[key];
              }else if(key.toUpperCase().slice(0,2) === 'DO'){
                this.mDO[key.slice(2)] = cval[key];
              }else if(key.toUpperCase().slice(0,2) === 'AI'){
                this.mAI[key.slice(2)] = cval[key];
              }else if(key.toUpperCase().slice(0,2) === 'AO') {
                this.mAO[key.slice(2)] = cval[key];
              }else if(key.toUpperCase().slice(0,2) === 'TI') {
                this.mTI[key.slice(2)] = cval[key];
              }else if(key.toUpperCase().slice(0,2) === 'TO'){
                this.mTO[key.slice(2)] = cval[key];
              }else{
                console.log('fatal: ', key);
                console.log('---------- 完整传递数据如下 ----------');
                console.log(cval);
                alert('出错了，打开console查看具体信息')
              }
            }
          },
          deep: true,
          immediate: true
        },
        newIoToAppend(cval, oval){
          /**
           * 当发现该值变为非空字符串时，为Module添加这个IO点。添加的位置为同一IO类型的最靠前空余点位。
           */
          if(cval === ''){
            return;
          }
          if(oval !== ''){
            console.log('警告： newIoToAppend可能有错误！检测到IoMaker未将其清空');
          }
          let temp = cval.split('--');
          if(temp.length !== 3){
            console.log("newIoToAppend数据格式不对，参考格式为 di-1-阀门1开，这里收到了:", cval);
            return;
          }
          let io_type = temp[0];
          let io_seq = temp[1];
          let io_name = temp[2];

          if(io_type.toUpperCase() === 'DI'){
            for(let ioIdx in this.mDI){
              if(this.mDI[ioIdx] === undefined){
                break;
              }
              if(this.mDI[ioIdx] === ''){
                this.mDI[ioIdx] = io_seq + '--' + io_name;
                break;
              }
            }
          }
          if(io_type.toUpperCase() === 'DO'){
            for(let ioIdx in this.mDO){
              if(this.mDO[ioIdx] === undefined){
                break;
              }
              if(this.mDO[ioIdx] === ''){
                this.mDO[ioIdx] = io_seq + '--' + io_name;
                break;
              }
            }
          }
          if(io_type.toUpperCase() === 'AI'){
            for(let ioIdx in this.mAI){
              if(this.mAI[ioIdx] === undefined){
                break;
              }
              if(this.mAI[ioIdx] === ''){
                this.mAI[ioIdx] = io_seq + '--' + io_name;
                break;
              }
            }
          }
          if(io_type.toUpperCase() === 'AO'){
            for(let ioIdx in this.mAO){
              if(this.mAO[ioIdx] === undefined){
                break;
              }
              if(this.mAO[ioIdx] === ''){
                this.mAO[ioIdx] = io_seq + '--' + io_name;
                break;
              }
            }
          }
          if(io_type.toUpperCase() === 'TI'){
            for(let ioIdx in this.mTI){
              if(this.mTI[ioIdx] === undefined){
                break;
              }
              if(this.mTI[ioIdx] === ''){
                this.mTI[ioIdx] = io_seq + '--' + io_name;
                break;
              }
            }
          }
          if(io_type.toUpperCase() === 'TO'){
            for(let ioIdx in this.mTO){
              if(this.mTO[ioIdx] === undefined){
                break;
              }
              if(this.mTO[ioIdx] === ''){
                this.mTO[ioIdx] = io_seq + '--' + io_name;
                break;
              }
            }
          }
          this.$emit('moduleiosupdate', this._getCurIoConfig());
        },
        varanConnModulePos: {
          handler(cval){
            this.$emit('varanposupdate', cval);
          },
          immediate: true
        }
      }
    }
</script>

<style scoped lang="scss">
  #module{
    width: 400px;
    height: auto;
    margin-top: 20px;
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
  .io-module{
    list-style: none;
    padding-left: 10px;
    .io-line{
      border-bottom: 1px red dotted;
      height: 35px;
      margin-right: 30px;
      .io-index{
        display: inline-block;
        /*line-height: 35px;*/
      }
      .alert{
        /* Overwrite default bootstrap style */
        width: 70%;
        display: inline-block;
        padding: .15rem 1.25rem;
        user-select: none;
        white-space: nowrap;
      }
      .io-name{
        display: inline-block;
      }
    }
  }
  .custom-control.custom-radio{
    margin-left: 5px;
  }
</style>
