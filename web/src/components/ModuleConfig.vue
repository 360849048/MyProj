<template>
  <div id="module">
    <ul id="DI" class="io-module">
      <li class="io-line" v-for="(item, index) in mDI" :key="index" v-if="index <= mDiAmount">
        <span class="badge badge-pill badge-success io-sequence">DI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item">
          {{item}}
        </div>
      </li>
    </ul>
    <ul id="DO" class="io-module">
      <li class="io-line" v-for="(item, index) in mDO" :key="index" v-if="index <= mDoAmount">
        <span class="badge badge-pill badge-danger io-sequence">DI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item">
          {{item}}
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
    export default {
        name: "module",
        props: [
          'moduleName',
          'ios'                        // 接收从父组件传递过来的json对象，用来配置点位  例如: {'di1': xxx, 'ao2': xxx}
        ],
        data(){
          return{
            mDI: {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''},
            mDO: {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''},
            mAI: {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''},
            mAO: {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''},
            mDiAmount: 0,
            mDoAmount: 0,
            mAiAmount: 0,
            mAoAmount: 0
          }
        },
        methods: {
          resetModuleIO(){
            this.mDI = {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''};
            this.mDO = {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''};
            this.mAI = {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
            this.mAO = {1: 'undefined', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
            this.mDiAmount = 0;
            this.mDoAmount = 0;
            this.mAiAmount = 0;
            this.mAoAmount = 0;
          }
        },
        watch: {
          moduleName: {
            handler(cval, oval){
              this.resetModuleIO();
              /*
              当 XX[?] === 'undefined'  时，该模块只拥有(?-1)个此类型的IO点。
              比如 mDI[1] === 0, 说明该模块没有DI点。
              再如 mDI[9] === 'undefined',说明该模块只有8个DI点。
              */
              if (cval.toUpperCase() === 'CTO163'){
                this.mDO[1] = '';
                this.mDoAmount = 16;
              }
              if (cval.toUpperCase() === 'CDM163'){
                this.mDI[1] = '';
                this.mDO[1] = '';
                this.mDI[9] = 'undefined';
                this.mDO[9] = 'undefined';
                this.mDiAmount = 8;
                this.mDoAmount = 8;
              }
            },
            deep: false,
            immediate: true,
          },
          ios: {
            handler(cval, oval){
              /**
               * 将传递过来的点位映射到模块点位上
               */
              // todo: 首先清空目前已存在的点位
              this.mDI = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''};
              this.mDO = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: ''};
              this.mAI = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
              this.mAO = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''};
              this.mDI[this.mDiAmount + 1] = 'undefined';
              this.mDO[this.mDoAmount + 1] = 'undefined';
              this.mAI[this.mAiAmount + 1] = 'undefined';
              this.mAO[this.mAoAmount + 1] = 'undefined';

              for(let key in cval){
                if (key.toUpperCase().slice(0, 2) === 'DI' ){
                  this.mDI[key.slice(-1)] = cval[key];
                }else if(key.toUpperCase().slice(0,2) === 'DO'){
                  this.mDO[key.slice(-1)] = cval[key];
                }else if(key.toUpperCase().slice(0,2) === 'AI'){
                  this.mAI[key.slice(-1)] = cval[key];
                }else if(key.toUpperCase().slice(0,2) === 'AO'){
                  this.mAO[key.slice(-1)] = cval[key];
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
          }
        }
    }
</script>

<style scoped lang="scss">
  #module{
    /*border: 1px gray dotted;*/
    width: 300px;
  }
  .io-module{
    list-style: none;
    padding-left: 10px;
    .io-line{
      border-bottom: 1px red dotted;
      height: 35px;
      .io-sequence{
        display: inline-block;
        /*line-height: 35px;*/
      }
      .alert{
        /* Overwrite default bootstrap style */
        display: inline-block;
        padding: .15rem 1.25rem;
        user-select: none;
      }
      .io-name{
        display: inline-block;
      }
    }
  }
</style>
