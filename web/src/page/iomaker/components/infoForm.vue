<template>
  <div id="infoform">
    <form>
      <div class="form-row">
        <div class="col-lg-4 mb-3">
          <label for="validationDefault01">评审单号</label>
          <input type="text" class="form-control" id="validationDefault01" autocomplete="off" v-model="evaluationNum">
        </div>
        <div class="col-lg-4 mb-3">
          <label for="validationDefault02">生产订单号</label>
          <input type="text" class="form-control" id="validationDefault02" required autocomplete="off" v-model="productionNum">
        </div>
        <div class="col-lg-4 mb-3">
          <label for="validationDefaultUsername"><span class="text-danger">*</span>机型</label>
          <input type="text" class="form-control" id="validationDefaultUsername" required autocomplete="off" v-model="immType"
          @change="handerImmTypeChange">
        </div>
      </div>
      <div class="form-row">
        <div class="col-lg-6 mb-3">
          <label for="validationDefault03">客户</label>
          <input type="text" class="form-control" id="validationDefault03" required autocomplete="off" v-model="customer">
        </div>
        <div class="col-lg-3 mb-3">
          <label for="validationDefault04">安全标准</label>
          <input type="text" class="form-control" id="validationDefault04" required autocomplete="off" v-model="safetyStandard">
        </div>
      </div>
      <div class="input-row">
        <label for="techInfo">技术条款</label>
        <textarea id="techInfo" class="form-control" aria-label="With textarea" v-model="technicalClause"></textarea>
      </div>
    </form>
    <hr>
    <div class="input-group">
      <div class="input-group-prepend">
        <label class="input-group-text" for="infoArea">设计说明</label>
      </div>
      <textarea class="form-control" id="infoArea" aria-label="With textarea" placeholder="这里不用填" v-model="designNote" style="height: 280px;"></textarea>
    </div>
    <button class="btn btn-secondary" id="autoFillBtn" @click="parseParams">自动填单</button>
  </div>
</template>

<script>
  /**
   * 数据处理逻辑：
   * 1.收集机器的基础信息，通过事件imminfochange发送到父组件
   * 2.触发imminfochange事件有如下几种情况：
   *   * 父组件传递下来的变量getInfo为true
   *   * immType变量输入框发生onchange事件
   *   * 从设计说明进行参数解析
   */
  export default {
    name: "info-form",
    props: ['getInfo'],
    data(){
      return{
        evaluationNum: '',
        productionNum: '',
        immType: '',
        customer: '',
        safetyStandard: '',
        technicalClause: '',
        designNote: ''
      }
    },
    methods: {
      _emitParams(_this){
        _this.$emit('imminfochange', {
          evaluationNum: _this.evaluationNum,
          productionNum: _this.productionNum,
          immType: _this.immType,
          customer: _this.customer,
          safetyStandard: _this.safetyStandard,
          technicalClause: _this.technicalClause,
          designNote: _this.designNote,
        });
      },
      parseParams(){
        /**
         * 从设计说明的文字this.designNote中提取出合同订单信息，并向父组件提交数据
         */
        if(this.designNote === ''){
          return;
        }
        let lines = this.designNote.split('\n');
        for(let line of lines){
          let temp = line.split('：');
          if(temp.length !== 2){
            continue;
          }
          let key = temp[0];
          // 去除首尾空格
          let value = temp[1].replace(/^\s+/, '');
          value = value.replace(/\s+$/, '');
          if(key.indexOf('客户名称') > -1){
            temp = value.split(' ');
            if(temp.length === 2){
              this.customer = temp[0];
              this.evaluationNum = temp[1];
            }

          }
          if(key.indexOf('机型') > -1){
            this.immType = value;
          }
          if(key.indexOf('规格') > -1){
            this.safetyStandard = value;
          }
          if(key.indexOf('生产订单') > -1){
            this.productionNum = value;
          }
        }
        this._emitParams(this);
      },
      handerImmTypeChange(){
        this._emitParams(this);
      }
    },
    watch: {
      getInfo(){
        if(this.getInfo === true){
          if(this.immType === ''){
            this.$notify.error({
              title: '漏填了重要信息',
              message: '注意啦，必须填写机器类型',
              position: 'top-left'
            });
          }
          this._emitParams(this);
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  #infoform{
    /*border: 1px gray dotted;*/
    padding: 15px;
    height: 100%;
    box-sizing: border-box;
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
  #BtnBox{
    display: flex;
    justify-content: flex-end;
    margin-top: 10px;
  }
  #techInfo{
    height: 300px;
  }
  #autoFillBtn{
    float: right;
  }
</style>
