<template>
  <div id="infoform">
    <form>
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="validationDefault01">评审单号</label>
          <input type="text" class="form-control" id="validationDefault01" autocomplete="off" v-model="evaluationNum">
        </div>
        <div class="col-md-4 mb-3">
          <label for="validationDefault02">生产订单号</label>
          <input type="text" class="form-control" id="validationDefault02" required autocomplete="off" v-model="productionNum">
        </div>
        <div class="col-md-4 mb-3">
          <label for="validationDefaultUsername"><span class="text-danger">*</span>机型</label>
          <input type="text" class="form-control" id="validationDefaultUsername" required autocomplete="off" v-model="immType">
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-6 mb-3">
          <label for="validationDefault03">客户</label>
          <input type="text" class="form-control" id="validationDefault03" required autocomplete="off" v-model="customer">
        </div>
        <div class="col-md-3 mb-3">
          <label for="validationDefault04">安全标准</label>
          <input type="text" class="form-control" id="validationDefault04" required autocomplete="off" v-model="safetyStandard">
        </div>
      </div>
      <div class="input-row">
        <label for="techInfo">技术条款</label>
        <textarea id="techInfo" class="form-control" aria-label="With textarea" v-model="technicalClause"></textarea>
      </div>
    </form>
    <!--<div id="BtnBox">-->
      <!--<button class="btn btn-danger ml-1 mr-1" @click="resetInfo">清空</button>-->
      <!--<button class="btn btn-primary ml-1 mr-1" @click="saveInfo">提交</button>-->
    <!--</div>-->
    <hr>
    <div class="input-group">
      <div class="input-group-prepend">
        <label class="input-group-text" for="infoArea">设计说明</label>
      </div>
      <textarea class="form-control" id="infoArea" aria-label="With textarea" placeholder="这里不用填" v-model="designNote" style="height: 100px;"></textarea>
    </div>
    <button class="btn btn-secondary" id="autoFillBtn" @click="parseParams">自动填单</button>
  </div>
</template>

<script>
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
      resetInfo(){
        this.evaluationNum = '';
        this.productionNum = '';
        this.immType = '';
        this.customer = '';
        this.safetyStandard = '';
        this.technicalClause = '';
        this.designNote = '';
        this.$emit('imminfochange', {
          evaluationNum: this.evaluationNum,
          productionNum: this.productionNum,
          immType: this.immType,
          customer: this.customer,
          safetyStandard: this.safetyStandard,
          technicalClause: this.technicalClause,
          designNote: this.designNote,
        });
      },
      saveInfo(){
        if(this.immType === ''){
          this.$notify.error({
            title: '错误',
            message: '必须填写机器类型',
            position: 'top-left'
          });
          return;
        }
        this.$emit('imminfochange', {
          evaluationNum: this.evaluationNum,
          productionNum: this.productionNum,
          immType: this.immType,
          customer: this.customer,
          safetyStandard: this.safetyStandard,
          technicalClause: this.technicalClause,
          evaluationNote: this.designNote,
        });
      },
      parseParams(){
        /**
         * 从设计说明的文字this.designNote中提取出合同订单信息
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
      }
    },
    watch: {
      getInfo(){
        if(this.getInfo === true){
          this.$emit('imminfochange', {
            evaluationNum: this.evaluationNum,
            productionNum: this.productionNum,
            immType: this.immType,
            customer: this.customer,
            safetyStandard: this.safetyStandard,
            technicalClause: this.technicalClause,
            designNote: this.designNote,
          });
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  #infoform{
    /*border: 1px gray dotted;*/
    padding: 5px;
    height: 700px;
    overflow: auto;
    &::-webkit-scrollbar{
      width: 6px;
      /*display: none;*/
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
    height: 120px;
  }
  #autoFillBtn{
    float: right;
  }
</style>
