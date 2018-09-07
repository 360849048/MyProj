<template>
  <div id="home">
    <h1>This is home page</h1>
    <span>{{msg}}</span>
    <i class="el-icon-edit"></i>
    <button class="btn btn-secondary" @click="createCookies">创建cookie</button>
    <button class="btn btn-secondary" @click="sendAJAX">发送AJAX请求</button>
  </div>
</template>

<script>
  export default{
    data(){
      return{
        msg: 'Hi, welcome!'
      }
    },
    methods:{
      createCookies(){
        document.cookie = 'username=J';
        alert('创建了cookie"username=J"');
      },
      sendAJAX(){
        $.ajax({
          data: {msg: this.msg},
          type: 'GET',
          url: 'foo',
          dataType: 'json',
          success: function(data){
            alert(data);
          },
          error: function(){
            alert('失败');
          }
        });
      }
    }
  }
</script>
