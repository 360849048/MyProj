<template>
  <div id="imm-type">
    <!-- type: ZEs ? ZE ? VE2s ? VE2 -->
    <div class="title">机型</div>
    <div class="custom-control custom-radio custom-control-inline"  v-for="eachType in types">
      <input class="custom-control-input" type="radio" name="type" :id="eachType" :value="eachType" v-model="type">
      <label class="form-check-label custom-control-label" :for="eachType">{{eachType}}</label>
    </div>

     <!--Lock: true or false  -->
    <div class="title">解锁按钮</div>
    <div class="custom-control custom-radio custom-control-inline"  v-for="eachLock in locks">
      <input class="custom-control-input" type="radio" name="lock" :id="eachLock" :value="eachLock" v-model="lock">
      <label class="form-check-label custom-control-label" :for="eachLock">{{eachLock}}</label>
    </div>

    <!-- inject: single or double -->
    <div class="title">注射</div>
    <div class="custom-control custom-radio custom-control-inline"  v-for="eachInject in injects">
      <input class="custom-control-input" type="radio" name="inject" :id="eachInject" :value="eachInject" v-model="inject">
      <label class="form-check-label custom-control-label" :for="eachInject">{{eachInject}}</label>
    </div>

    <!-- standard: CE or not -->
    <div class="title">标准</div>
    <div class="custom-control custom-radio custom-control-inline"  v-for="eachStandard in standards">
      <input class="custom-control-input" type="radio" name="standard" :id="eachStandard" :value="eachStandard" v-model="standard">
      <label class="form-check-label custom-control-label" :for="eachStandard">{{eachStandard}}</label>
    </div>
  </div>

</template>

<script>

  export default {
    name: "imm-type",
    data(){
      return{
        types: ["ZEs", "ZE", "VE2s", "VE2"],
        locks: ["lock","nolock"],
        injects: ["single", "double"],
        standards: ["noCE", "CE"],

        type: "ZEs",
        lock: "lock",
        inject: "single",
        standard: "noCE"
      }
    },
    watch: {
      type: function (newType, oldType){
        this.$emit("changeType", this.type);
      },
      lock: function(newLock, oldLock){
        this.$emit("changeLock", this.lock);
      },
      inject: function(newInject, oldInject){
        this.$emit("changeInject", this.inject);
      },
      standard: function(newsStandard, oldStandard){
        this.$emit("changeStandard", this.standard);
      }
    },
    mounted: function(){
      this.$emit("changeType", this.type);
      this.$emit("changeLock", this.lock);
      this.$emit("changeInject", this.inject);
      this.$emit("changeStandard", this.standard);
    }
  }
</script>

<style scoped lang="scss">
  .title{
    background-color: #eee;
    text-align: center;
    margin-top: 5px;
    border-radius: 3px;
    color: #0ca2d5
  }
  .custom-control-inline{
    margin: 0;
    padding: 10px;
  }
  .custom-control-label{
    width: 5rem;
    transition: all 1s;
    border-left: 1.5rem solid transparent;
    border-right: 1.5rem solid transparent;
    border-bottom: 0.1rem solid transparent;
    border-radius: 20%;
    &:hover{
       /*background: rgba(181, 222, 255, 0.31);*/
       /*box-shadow: 0 0 30px rgba(108, 151, 255, 0.62);*/
       border-bottom: 0.1rem solid rgba(108, 151, 255, 0.62);
     }
  }
  .custom-control-label::before{
    transition: all 0.5s;
  }
</style>
