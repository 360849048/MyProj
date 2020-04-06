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
      </div>
      <label for="random_codes">5级随机码</label>
      <input id="random_codes" type="text" v-model="randomCodes"  @keydown.enter="getPwd5">
      <button class="btn btn-primary" @click="getPwd5">获取5级密码</button>
      <!-- 文件上传测试 -->
      <hr>
      <form action="/api/srctransfer" enctype="multipart/form-data" method="POST">
        <label>文件上传</label>
        <input id="fileUpload" type="file" name="file" multiple="multiple">
        <input type="submit" value="上传">
      </form>
      <hr>
      <!-- 使用ajax方法来上传文件 -->
      <button @click="uploadjqAjax">jQuery上传</button>
      <button @click="uploadaxAjax">axios上传</button>
  </div>

  </div>
</template>
<script>
  import axios from 'axios'
  import ImmType from './components/ImmType'

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
        },
        ios: {di1: '可编程io输入1', do1: '可编程io输出1'},
        module: 'cdm163',
        randomCodes: '',
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
      getPwd5 () {
        if (this.randomCodes.search(/\d{10}$/) !== 0) {
          alert("5级随机码长度必须是10，且都是0-9的数字");
          return;
        }
        axios.get(`/api/getpwd5?randomcodes=${this.randomCodes}`).then(res => {
          res = res.data;
          console.log(res);
          alert('5级密码为: ' + res);
        }).catch(e => {
          console.log(e);
        })
      },
      uploadjqAjax () {
        let formData = new FormData();
        let fileUpload = document.querySelector("#fileUpload");

        formData.append("username", "J");
        formData.append("gender", "male");
        // Only support 1 file at a time.
        formData.append("file", fileUpload.files[0]);

        $.ajax({
          url: '/api/srctransfer',
          dataType: 'json',
          type: 'POST',
          data: formData,
          processData : false, // 使数据不做处理
          contentType : false, // 不要设置Content-Type请求头
          success: function(data){
            console.log(data);
          },
          error: function(res){
            console.log(res);
          }
        })
      },
      uploadaxAjax () {
        let formData = new FormData();
        let fileUpload = document.querySelector("#fileUpload");

        // Only support 1 file at a time.
        formData.append("file", fileUpload.files[0]);

        const config = {
           headers: {
             "Content-Type": "multipart/form-data;boundary="+new Date().getTime()
           }
        };
        axios.post("/api/srctransfer", formData, config).then(function(res){
          console.log(res);
        }).catch(function(err){
          console.log(err);
        })
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
  .file-upload-btn {
    position: relative;
    display: inline-block;
    width: 100px;
    overflow: hidden;
    cursor: pointer;
    label {
      background-color: #c69500;
      color: #eee;
      border-radius: 5px;
      box-shadow: 1px 1px 5px 1px #ccc;
      padding: 10px;
      cursor: inherit;
    }
    input {
      position: absolute;
      top: 0;
      right: 0;
      opacity: 0;
      cursor: inherit;
    }
  }
</style>
