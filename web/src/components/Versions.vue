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
        <td scope="col">{{msg.client}}</td>
        <td scope="col">{{msg.version}}</td>
        <td scope="col">{{msg.date}}</td>
        <td scope="col">{{msg.base}}</td>
        <td scope="col">{{msg.record}}</td>
        <td scope="col">{{msg.reason}}</td>
        <td scope="col">{{msg.remark}}</td>
        <td scope="col">{{msg.author}}</td>
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
            client: 'Zhafir',
            version: 'V05_38_20',
            date: '2018.06.18',
            base: 'V05_38_00',
            record: '紧急bug修复，原标准程序托模无法保持',
            reason: '标准程序',
            remark: '',
            author: 'CX'
          }
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
            console.log(_this.softVers);
          },
          error: function(){
            console.log('AJAX请求无法获取Version列表');
          }
        });
      }
    }
  }
</script>
