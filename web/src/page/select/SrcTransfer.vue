<template>
  <div id="srctransfer">
    <div class="container">
      <div class="row justify-content-around">
        <div class="col-md-5" id="imm-type">
          <imm-type
                    @changeType="getType"
                    @changeLock="getLock"
                    @changeInject="getInject"
                    @changeStandard="getStandard">
          </imm-type>
        </div>
      </div>

      <label for="random_codes">5级随机码</label>
      <input id="random_codes" type="text" v-model="randomCodes"  @keydown.enter="getPwd5">
      <button class="btn btn-primary" @click="getPwd5">获取5级密码</button>

  </div>
  </div>
</template>
<script>
  import axios from 'axios'
  import ImmType from './components/ImmType'

  export default{
    components:{
      ImmType,
    },
    data(){
      return{
        immParams: {
          type: '',
          lock: '',
          inject: '',
          standard: ''
        },
        ios: {di1: '可编程io输入1', do1: '可编程io输出1'},
        module: 'cdm163',
        randomCodes: '',
      }
    },
    methods: {
      getType(type){
        this.immParams.type = type;
      },
      getLock(lock){
        this.immParams.lock = lock;
      },
      getInject(inject){
        this.immParams.inject = inject;
      },
      getStandard(standard){
        this.immParams.standard = standard;
      },
      getPwd5 () {
        if (this.randomCodes.search(/\d{10}$/) !== 0) {
          alert("5级随机码长度必须是10，且都是0-9的数字");
          return;
        }
        axios.get(`/api/getpwd5?randomcodes=${this.randomCodes}`).then(res => {
          res = res.data;
          console.log(res);
          alert('5级密码为: ' + res);
        }).catch(e => {
          console.log(e);
        })
      }
    }
  }
</script>
<style lang="scss" scoped>
  #imm-type{
    user-select: none;
  }
  #imm-params{
    // height: 150px;
  }
</style>
