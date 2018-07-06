<template>
  <div id="module">
    <ul id="DI" class="io-module">
      <li class="io-line" v-for="(item, index) in mDI" :key="index" v-if="index <= mDiAmount"
          :data-index="index" data-type="di"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-success io-sequence">DI&nbsp;&nbsp;{{index}}</span>
        <div class="alert alert-primary io-name" role="alert" v-if="item">
          {{item}}
        </div>
      </li>
    </ul>
    <ul id="DO" class="io-module">
      <li class="io-line" v-for="(item, index) in mDO" :key="index" v-if="index <= mDoAmount"
          :data-index="index" data-type="do"
          @dragover.prevent="" @drop="dropIO">
        <span class="badge badge-pill badge-danger io-sequence">DO&nbsp;&nbsp;{{index}}</span>
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
        'moduleName'
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
        },
        dropIO(e){
          let ioInfo = e.dataTransfer.getData('ioInfo').split('--');
          if(ioInfo.length !== 3){
            console.log(ioInfo, '---数据格式出错');
            return;
          }
          // 解析从父组件拖拽传递过来的数据
          let ioType = ioInfo[0];
          let ioSeq = ioInfo[1];
          let ioName = ioInfo[2];
          // 获取拖拽目的地的IO类型
          let thisType = e.target.getAttribute('data-type');
          if(ioType.toUpperCase() !== thisType.toUpperCase()){
            console.log("类型不一致，无法拖放");
            return;
          }
          if(ioType.toUpperCase() === 'DI'){
            let ioIdx = e.target.getAttribute('data-index');
            this.mDI[ioIdx] = ioName;
          }else if(ioType.toUpperCase() === 'DO'){
            let ioIdx = e.target.getAttribute('data-index');
            this.mDO[ioIdx] = ioName;
          }
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
