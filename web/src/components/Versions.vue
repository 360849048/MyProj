<template>
  <div id="versions">
    <h1>This is software-versions page</h1>
    <button class="btn btn-primary" @click="getVers(1, 100)"></button>
    <table class="table table-hover" v-loading="loading">
      <thead>
      <tr>
        <th scope="col">客户</th>
        <th scope="col">版本</th>
        <th scope="col">更改日期</th>
        <th scope="col">原版本</th>
        <th scope="col">内容</th>
        <th scope="col">原因</th>
        <th scope="col">备注</th>
        <th scope="col">更改人</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(msg, index) in softVers" :key="index">
        <td scope="col"><div>{{msg.client}}</div></td>
        <td scope="col"><div>{{msg.version}}</div></td>
        <td scope="col"><div>{{msg.date}}</div></td>
        <td scope="col"><div>{{msg.base}}</div></td>
        <td scope="col"><div>{{msg.record}}</div></td>
        <td scope="col"><div>{{msg.reason}}</div></td>
        <td scope="col"><div>{{msg.remark}}</div></td>
        <td scope="col"><div>{{msg.author}}</div></td>
      </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
  export default{
    name: 'versions',
    data(){
      return{
        loading: false,
        softVers: {
          1: {
            client: 'Zhafir',
            version: 'V05_38_50',
            date: '2018.08.18',
            base: 'V05_38_20',
            record: '新增较多功能',
            reason: '标准程序',
            remark: '',
            author: 'CX'
          },
          2: {
            client: '美视伊',
            version: 'V05_15_10',
            date: '2017.01.18',
            base: 'V05_15_15',
            record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
            reason: '合同',
            remark: '',
            author: '王何宇'
          },
        }
      }
    },
    methods: {
      getVers(firstId, lastId){
        let _this = this;
        $.ajax({
          url: "/queryversions",
          type: 'GET',
          dataType: 'json',
          data: {"start": firstId, 'end': lastId},
          beforeSend: function(){
            _this.loading = true;
          },
          complete: function() {
            _this.loading = false;
          },
          success: function(data){
            _this.softVers = data;
          },
          error: function(){
            console.log('AJAX请求无法获取Version列表');
          }
        });
      }
    }
  }
</script>
<style scoped>
  td div{
    height: 30px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 600px;
  }
  @media screen and (max-width: 1000px){
    td div{
      max-width: 300px !important;
    }
  }
  td div:hover{
    overflow: auto;
    white-space: normal;
    height: auto;
  }
</style>
