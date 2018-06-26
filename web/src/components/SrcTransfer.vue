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
        <button class="btn btn-primary" type="submit" @click="useJquery">Button</button>
      </div>
    </div>
  </div>
</template>
<script>
  import ImmType from './ImmType'

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
        }
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
        alert('ok');
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
