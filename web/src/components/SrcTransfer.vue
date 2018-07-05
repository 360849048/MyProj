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

        <div class="col-md-6" id="imm-params">
          <imm-config></imm-config>
        </div>

      </div>

      <div class="row">
        <button class="btn btn-primary" type="submit" @click="useJquery">切换模块</button>
        <button class="btn btn-primary" type="submit" @click="foo">修改点位</button>
        <button class="btn btn-primary" type="submit" @click="bar">撤销</button>
      </div>
      <div class="row">
        <module-config
          :module-name="module"
          :ios="ios">
        </module-config>
      </div>
    </div>
  </div>
</template>
<script>
  import ImmType from './ImmType'
  import ImmConfig from './ImmConfig'
  import ModuleConfig from './ModuleConfig'

  export default{
    components:{
      ImmType,
      ImmConfig,
      ModuleConfig
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
        module: 'cdm163'
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
      foo(){
        this.ios = {do1: '阀门1开', do2: '阀门2开'};
      },
      bar(){
        console.log('hi');
      },
      useJquery(){
        // console.log($.ajax({
        //   url: "/foo",
        //   type: 'POST',
        //   data: this.immParams,
        //   dataType: 'json',
        //   success: function(data){
        //     console.log(data);
        //   },
        //   error: function(){
        //     console.log('Error!!!');
        //   }
        // }));
        this.module = 'cto163';
        this.ios = {};
        // this.ios.do2 = 'valve 3 open';
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
