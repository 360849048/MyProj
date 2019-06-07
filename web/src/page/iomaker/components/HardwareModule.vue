<template>
  <div id="hardware-module">
    <ul id="DI" class="io-module">
      <li class="io-line"
          v-for="(item, index) in mDI"
          :key="index"
          :data-index="index"
          data-type="DI"
          v-if="index <= mDiAmount"
          @dragover.prevent=""
          @drop="dropIO"
      >
        <span class="badge badge-pill badge-success io-index">DI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert"
             v-if="item"
             @dblclick="dblclickIO('DI', index, item)"
        >
          {{searchIONameByIdx('DI', item)}}
        </div>
      </li>
    </ul>
    <ul id="DO" class="io-module">
      <li class="io-line"
          v-for="(item, index) in mDO"
          :key="index"
          :data-index="index"
          data-type="DO"
          v-if="index <= mDoAmount"
          @dragover.prevent=""
          @drop="dropIO"
      >
        <span class="badge badge-pill badge-danger io-index">DO&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert"
             v-if="item"
             @dblclick="dblclickIO('DO', index, item)"
        >
          {{searchIONameByIdx('DO', item)}}
        </div>
      </li>
    </ul>
    <ul id="AI" class="io-module">
      <li class="io-line"
          v-for="(item, index) in mAI"
          :key="index"
          :data-index="index"
          data-type="AI"
          v-if="index <= mAiAmount"
          @dragover.prevent=""
          @drop="dropIO"
      >
        <span class="badge badge-pill badge-info io-index">AI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert"
             v-if="item"
             @dblclick="dblclickIO('AI', index, item)"
        >
          {{searchIONameByIdx('AI', item)}}
        </div>
      </li>
    </ul>
    <ul id="AO" class="io-module">
      <li class="io-line"
          v-for="(item, index) in mAO"
          :key="index"
          :data-index="index"
          data-type="AO"
          v-if="index <= mAoAmount"
          @dragover.prevent=""
          @drop="dropIO"
      >
        <span class="badge badge-pill badge-warning io-index">AO&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert"
             v-if="item"
             @dblclick="dblclickIO('AO', index, item)"
        >
          {{searchIONameByIdx('AO', item)}}
        </div>
      </li>
    </ul>
    <ul id="TI" class="io-module">
      <li class="io-line"
          v-for="(item, index) in mTI"
          :key="index"
          :data-index="index"
          data-type="TI"
          v-if="index <= mTiAmount"
          @dragover.prevent=""
          @drop="dropIO"
      >
        <span class="badge badge-pill badge-info io-index">TI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert"
             v-if="item"
             @dblclick="dblclickIO('TI', index, item)"
        >
          {{searchIONameByIdx('TI', item)}}
        </div>
      </li>
    </ul>
    <ul id="TO" class="io-module">
      <li class="io-line"
          v-for="(item, index) in mTO"
          :key="index"
          :data-index="index"
          data-tpye="TO"
          v-if="index <= mToAmount"
          @dragover.prevent=""
          @drop="dropIO"
      >
        <span class="badge badge-pill badge-warning io-index">TO&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert"
             v-if="item"
             @dblclick="dblclickIO('To', index, item)"
        >
          {{searchIONameByIdx('TO', item)}}
        </div>
      </li>
    </ul>
    <!-- 单独处理CIV512等连接模块 -->
    <div v-if="moduleName.toUpperCase() === 'CIV512' || moduleName.toUpperCase() === 'CIV521'">
      <p class="h1">
        已激活扩展该底板，连接模块是：{{moduleName}}
      </p>
      <div v-show="curBoard === 3">
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
      <div v-show="curBoard === 4">
        <hr>
        <i class="fa fa-exclamation text-danger" aria-hidden="true"></i>
        <span>底板三后端功能尚未开发完全，无法写入IO表和硬件配置</span>
      </div>

    </div>
  </div>
</template>

<script>
  /**
   * 各个子模块视图层的更新应当由props来进行，避免某些函数的反复调用
   */
  export default {
    name: "hardware-module",
    props: {
      moduleName: String,
      ioConfig: Object,
      allIO: Object,
      ioInfoLoaded: Boolean,
      curBoard: Number,
      newIoToAppend: String,
    },
    data () {
      return{
        // 当 XX[?] === undefined  时，该模块只拥有(?-1)个此类型的IO点。
        // 比如 mDI[1] === undefined, 说明该模块没有DI点。
        // 再如 mDI[9] === undefined,说明该模块只有8个DI点。
        mDI: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '',
          9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''},
        mDO: {1: undefined, 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '',
          9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''},
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
        varanConnModulePos: 0,
      }
    },
    methods: {
      _initModuleIO(moduleName) {
        /**
         * 根据当前的模块名，初始化模块信息（清空IO配点信息）
         */
        this.mDI = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '',
          9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''
        };
        this.mDO = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '',
          9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''
        };
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

        switch (moduleName.toUpperCase()) {
          case 'CTO163':
            this.mDoAmount = 16;
            break;
          case 'CDM163':
            this.mDiAmount = 8;
            this.mDoAmount = 8;
            break;
          case 'CIO021':
            this.mDiAmount = 8;
            this.mDoAmount = 8;
            this.mAiAmount = 3;
            this.mAoAmount = 2;
            break;
          case 'CDI163':
            this.mDiAmount = 16;
            break;
          case 'CAI888':
            this.mTiAmount = 8;
            this.mToAmount = 8;
            break;
        }
        if (moduleName.toUpperCase() === 'CIO011') {
          this.mDiAmount = 8;
          this.mDoAmount = 8;
          this.mAiAmount = 2;
          this.mAoAmount = 1;
        }
        if (this.mDiAmount < 16) {
          this.mDI[this.mDiAmount + 1] = undefined;
        }
        if (this.mDoAmount < 16) {
          this.mDO[this.mDoAmount + 1] = undefined;
        }
        if (this.mAiAmount < 16) {
          this.mAI[this.mAiAmount + 1] = undefined;
        }
        if (this.mAoAmount < 16) {
          this.mAO[this.mAoAmount + 1] = undefined;
        }
        if (this.mTiAmount < 16) {
          this.mTI[this.mTiAmount + 1] = undefined;
        }
        if (this.mToAmount < 16) {
          this.mTO[this.mToAmount + 1] = undefined;
        }
      },
      _configModuleIO (ioConfig) {
        for(let key in ioConfig){
          switch (key.slice(0, 2)) {
            case 'DI':
              this.mDI[key.slice(2)] = ioConfig[key];
              break;
            case 'DO':
              this.mDO[key.slice(2)] = ioConfig[key];
              break;
            case 'AI':
              this.mAI[key.slice(2)] = ioConfig[key];
              break;
            case 'AO':
              this.mAO[key.slice(2)] = ioConfig[key];
              break;
            case 'TI':
              this.mTI[key.slice(2)] = ioConfig[key];
              break;
            case 'TO':
              this.mTO[key.slice(2)] = ioConfig[key];
              break;
            default:
              console.log(ioConfig);
              alert('出错了，打开console查看具体信息')
          }
        }
      } ,
      dblclickIO (ioType, moduleIoIdx, ioIdx) {
        let ioConfig = JSON.parse(JSON.stringify(this.ioConfig));
        let key = ioType + moduleIoIdx;
        try {
          delete ioConfig[key];
        } catch (e) {
          alert('删除模块配点错误！见控制台');
          console.log(e);
        }
        this.$emit('moduleiosupdate', ioConfig);
      },
      dropIO (e) {
        let ioConfig = JSON.parse(JSON.stringify(this.ioConfig));
        let ioInfo = e.dataTransfer.getData('ioInfo');
        let [fromIoType, item] = ioInfo.split('--');
        item = parseInt(item);
        let toIoType = e.target.getAttribute('data-type');
        let moduleIoIdx = e.target.getAttribute('data-index');
        let key = toIoType + moduleIoIdx;

        if (toIoType !== fromIoType || key in ioConfig) {
          // IO类型不相同，或已经被占用，不允许配置
          return;
        }
        ioConfig[key] = item;
        this.$emit('moduleiosupdate', ioConfig);
      },
      searchIONameByIdx (ioType, idx) {
        let retval = idx;
        if (this.ioInfoLoaded) {
          try {
            retval = this.allIO[ioType][idx - 1];
          } catch (e) {
            alert('配置的IO点序号超出范围！详情见控制台');
            console.log(e)
          }
        }
        return retval;
      }
    },
    watch: {
        moduleName: {
          /**
           * 根据moduleName初始化模块IO点（调用_initModuleIO依次初始化mDiAmount,mDoAmount,mAiAmount,mAoAmount,mDI,mDO,mAI,mAO）
           */
          handler(cval){
            this._initModuleIO(cval);
            // 不同的模块但是配置了相同的IO点，不执行下面方法可能导致配点不显示
            this._configModuleIO(this.ioConfig)
          },
          deep: false,
          immediate: true,
        },
        ioConfig: {
          /**
           * 将ioConfig信息写入到mDI,mDO,mAI,mAO,mTI,mTO中。
           */
          handler(cval){
            this._initModuleIO(this.moduleName);
            this._configModuleIO(cval);
          },
          deep: true,
          immediate: true
        },
        varanConnModulePos: {
          handler(cval){
            this.$emit('varanposupdate', cval);
          },
          immediate: true
        },
        newIoToAppend(cval, oval){
          if(cval === '' || this.moduleName === ''){
            return;
          }
          if(oval !== ''){
            console.log('警告： newIoToAppend可能有错误！检测到IoMaker未将其清空');
          }
          try {
            let [io_type, item] = cval.split('--');
            item = parseInt(item);
            let ioConfig = JSON.parse(JSON.stringify(this.ioConfig));

            switch (io_type) {
              case 'DI':
                for (let index in this.mDI) {
                  if (this.mDI[index] === undefined) {
                    break;
                  }
                  if (this.mDI[index] === '') {
                    ioConfig['DI' + index] = item;
                    break;
                  }
                }
                break;
              case 'DO':
                for (let index in this.mDO) {
                  if (this.mDO[index] === undefined) {
                    break;
                  }
                  if (this.mDO[index] === '') {
                    ioConfig['DO' + index] = item;
                    break;
                  }
                }
                break;
              case 'AI':
                for (let index in this.mAI) {
                  if (this.mAI[index] === undefined) {
                    break;
                  }
                  if (this.mAI[index] === '') {
                    ioConfig['AI' + index] = item;
                    break;
                  }
                }
                break;
              case 'AO':
                for (let index in this.mAO) {
                  if (this.mAO[index] === undefined) {
                    break;
                  }
                  if (this.mAO[index] === '') {
                    ioConfig['AO' + index] = item;
                    break;
                  }
                }
                break;
              case 'TI':
                for (let index in this.mTI) {
                  if (this.mTI[index] === undefined) {
                    break;
                  }
                  if (this.mTI[index] === '') {
                    ioConfig['TI' + index] = item;
                    break;
                  }
                }
                break;
              case 'TO':
                for (let index in this.mTO) {
                  if (this.mTO[index] === undefined) {
                    break;
                  }
                  if (this.mTO[index] === '') {
                    ioConfig['TO' + index] = item;
                    break;
                  }
                }
                break;
            }
            this.$emit('moduleiosupdate', ioConfig);
          } catch (e) {
            alert('出现了未知错误，请查看控制台')
            console.log(e);
          }
        },
      }
  }
</script>

<style scoped lang="scss">
  #hardware-module{
    width: 400px;
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
      display: grid;
      grid-template-columns: 20% 80%;
      align-items: center;
      justify-items: left;
      .io-index{
        width: 80%;
      }
      .io-name{
        width: 90%;
        display: inline-block;
        padding: .15rem 1rem;
        user-select: none;
        margin-bottom: 0 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        &:hover {
          overflow: visible;
        }
      }
    }
  }
  .custom-control.custom-radio{
    margin-left: 5px;
  }
</style>
