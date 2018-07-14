<template>
    <div id="srcmaker">
      <div class="container-fluid">
        <div class="row">
          <!-- IO选择区域 -->
          <div class="col-sm-8">
            <io-list></io-list>
          </div>
          <!-- 模块显示区 -->
          <div class="col-sm-4" id="module_area">
            <module></module>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  import IoList from './iomaker/IoList'
  import Module from './iomaker/Module'

  export default {
    components:{
      IoList,
      Module
    },
  }
</script>
<style scoped>

</style>
