<template>
  <div id="srctransfer">
    <div class="container">
      <div class="row justify-content-around">
        <div class="col-md-5" id="imm-type">
          <imm-type @changeType="getType"
                    @changeLock="getLock"
                    @changeInject="getInject"
                    @changeStandard="getStandard">
          </imm-type>
        </div>

        <div class="col-md-6" id="imm-params">
          <div class="card text-white bg-success mb-6">
            <div class="card-header">Params Select</div>
            <div class="card-body">
              <h5 class="card-title">Success card title</h5>
              <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            </div>
          </div>
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
      ImmType
    },
    data(){
      return{
        type: "",
        lock: "",
        inject: "",
        standard: ""
      }
    },
    methods: {
      getType(type){
        this.type = type;
      },
      getLock(lock){
        this.lock = lock;
      },
      getInject(inject){
        this.inject = inject;
      },
      getStandard(standard){
        this.standard = standard;
      },
      useJquery(){
        // $.ajax({
        //   url: 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su',
        //   data:{wd: 'ok'},
        //   dataType: 'jsonp',
        //   jsonp: 'cb',
        //   jsonpCallback: 'jshow',
        //   type: 'GET',
        //   success: function(result){
        //     console.log(result);
        //   },
        //   error: function(xhr){
        //     console.log('Failed');
        //   }
        // })
        console.log($.ajax({
          url: "/foo",
          type: 'POST',
          data: {
            'type': this.type,
            'lock': this.lock
          }
        }));
      }
    }
  }
</script>
<style lang="scss" scoped>
  #imm-type{
    border: 1px dotted gray;
    user-select: none;
  }
  #imm-params{
    border: 1px dotted gray;
    // height: 150px;
  }
</style>
