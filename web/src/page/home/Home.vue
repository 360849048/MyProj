<template>
  <div id="home">
    <h1>This is home page</h1>
    <i class="el-icon-edit"></i>
    <button class="btn btn-secondary" @click="createCookies">创建cookie</button>
    <button class="btn btn-secondary" @click="sendAJAX">发送AJAX请求</button>
    <div class="row"></div>
      <form class="col-3" action="/api/foo" method="post" target="id_iframe">
        <div class="form-group">
          <label for="exampleInputEmail1">Account</label>
          <input type="text" class="form-control" id="exampleInputEmail1" placeholder="Enter username" name="username" autocomplete="off">
          <small id="accountHelp" class="form-text text-muted">We'll never share your account with anyone else.</small>
        </div>
        <div class="form-group">
          <label for="exampleInputPassword1">Password</label>
          <input type="password" class="form-control" id="exampleInputPassword1" name="password" autocomplete="off" placeholder="Password">
        </div>
        <div class="form-check">
          <input type="checkbox" class="form-check-input" id="exampleCheck1">
          <label class="form-check-label" for="exampleCheck1">Check me out</label>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    {{testData}}
    <iframe id="id_iframe" name="id_iframe" style="display: none"></iframe>
    <button @click="testCROS">halo?</button>
  </div>

</template>

<script>
  import { mapState } from 'vuex'


  export default{
    data(){
      return{
        ajaxMsg: 'Hi, welcome!'
      }
    },
    methods:{
      createCookies(){
        document.cookie = 'username=J';
        alert('创建了cookie"username=J"');
      },
      sendAJAX(){
        $.ajax({
          data: {"msg": this.ajaxMsg},
          type: 'GET',
          url: '/api/foo',
          // dataType: 'json',
          success: function(data){
            alert(data);
          },
          error: function(){
            alert('失败');
          }
        });
      },
      testCROS () {
        $.ajax({
          url: 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su',
          data:{wd: "hello world"},
          jsonp: 'cb',
          dataType: 'jsonp',
          type: 'GET',
          success: function(result){
            console.log(result)
          },
          error: function(xhr){
            console.log('Failed');
          }
        })
      }
    },
    computed: {
      ...mapState(['testData'])
    }
  }
</script>
