<template>
  <div id="infoform">
    <form>
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="validationDefault01">评审单号</label>
          <input type="text" class="form-control" id="validationDefault01" autocomplete="off">
        </div>
        <div class="col-md-4 mb-3">
          <label for="validationDefault02">生产订单号</label>
          <input type="text" class="form-control" id="validationDefault02" required autocomplete="off">
        </div>
        <div class="col-md-4 mb-3">
          <label for="validationDefaultUsername">机型</label>
          <input type="text" class="form-control" id="validationDefaultUsername" aria-describedby="inputGroupPrepend2" required autocomplete="off">
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-6 mb-3">
          <label for="validationDefault03">客户</label>
          <input type="text" class="form-control" id="validationDefault03" required autocomplete="off">
        </div>
        <div class="col-md-3 mb-3">
          <label for="validationDefault04">安全标准</label>
          <input type="text" class="form-control" id="validationDefault04" required autocomplete="off">
        </div>
      </div>
      <div class="input-row">
        <label for="techInfo">技术条款</label>
        <textarea id="techInfo" class="form-control" aria-label="With textarea"></textarea>
      </div>
      <hr>
      <button class="btn btn-primary">提交验证信息</button>
    </form>
    <hr>
    <div class="input-group">
      <div class="input-group-prepend">
        <label class="input-group-text" for="infoArea">流程信息</label>
      </div>
      <textarea class="form-control" id="infoArea" aria-label="With textarea" style="height: 100px;"></textarea>
    </div>
    <button class="btn btn-secondary" id="autoFillBtn">自动填单</button>
  </div>
</template>

<script>
    export default {
        name: "info-form"
    }
</script>

<style lang="scss" scoped>
  #infoform{
    /*border: 1px gray dotted;*/
    height: 800px;
    overflow: auto;
    &::-webkit-scrollbar{
      display: none;
    }
  }
  #techInfo{
    height: 120px;
  }
  #autoFillBtn{
    float: right;
  }
</style>
