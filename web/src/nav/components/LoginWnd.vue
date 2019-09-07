<template>
  <Fade>
    <div class="shade" v-if="showWnd" @mousedown.self="hideLoginWnd">
    <div class="login-wnd" ref="loginWnd">
    <div class="titlebar" @mousedown="moveLoginWnd">
      <p class="login-title">登录</p>
      <i class="fa fa-times fa-2x btn-exit" aria-hidden="true" @click="hideLoginWnd"></i>
    </div>
    <div class="work-area">
      <form class="username" onsubmit="return false;">
        <label for="username">用户：</label>
        <input id="username" type="text" v-model="account" @keydown.enter="userLogin">
      </form>
      <form class="password" onsubmit="return false;">
        <label for="password">密码：</label>
        <input id="password" type="password" v-model="password" @keydown.enter="userLogin">
      </form>
      <div class="btns">
        <button class="btn btn-outline-primary" @click="userLogin">确认</button>
        <button class="btn btn-outline-secondary" @click="resetUserInfo">重置</button>
      </div>
    </div>
  </div>
  </div>
  </Fade>
</template>

<script>
  import axios from 'axios'
  import { mapState, mapActions} from 'vuex'
  import Fade from '@/common/animation/Fade'

  export default {
    name: "loginwnd",
    props: {
      showWnd: Boolean
    },
    components: {
      Fade,
    },
    computed: {
    },
    data () {
      return {
        account: '',
        password: ''
      }
    },
    methods: {
      ...mapActions(['login']),
      moveLoginWnd (e) {
        let loginWnd = this.$refs.loginWnd;
        let clientX = loginWnd.offsetLeft;
        let clientY = loginWnd.offsetTop;
        let originMouseX = e.x;
        let originMouseY = e.y;
        let eventMov = function (e) {
          let curMouseX = e.x;
          let curMouseY = e.y;
          loginWnd.style.left = curMouseX - originMouseX + clientX + 'px';
          loginWnd.style.top = curMouseY - originMouseY + clientY + 'px';
        };
        let rmEventMov = function () {
          try {
            document.removeEventListener('mousemove', eventMov);
            document.removeEventListener('mouseup', rmEventMov);
          } catch (e) {
            console.log(e);
          }
        };
        document.addEventListener('mousemove', eventMov);
        document.addEventListener('mouseup', rmEventMov);
      },
      userLogin () {
        axios.post('/api/login', {
          account: this.account,
          pwd: this.password,
        }).then(res => {
          res = res.data;
          if (res.status === 'success') {
            this.hideLoginWnd();
            let userInfo = {'account': this.account, 'username': res.username, 'superAuth': res.sp};
            this.login(userInfo);
            this.$message({
              message: '登录成功',
              type: 'success'
            });
            this.resetUserInfo();
          } else {
            this.$message({
              message: '密码或账号错误',
              type: 'error'
            });
          }
        }).catch(err => {console.log(err)})
      },
      resetUserInfo () {
        this.account = '';
        this.password = '';
      },
      hideLoginWnd () {
        this.$emit("hidewnd")
      }
    },
    mounted () {

    }
  }
</script>

<style scoped lang="scss">
  .shade {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(100, 100, 100, .5);
  }
  .login-wnd {
    $wndWidth: 400px;
    $wndHeight: 250px;
    $titleHeight: 15%;
    position: absolute;
    left: 50%;
    top: 50%;
    width: $wndWidth;
    height: $wndHeight;
    transform: translate(-$wndWidth/2, -$wndHeight/2);
    box-shadow: 0 0 20px #666;
    background: #fff;
    border-radius: 5px;
    @media screen and(max-width: $wndWidth){
      left: 0;
      width: 100%;
      transform: translate(0, -$wndHeight/2);
    }
    .titlebar {
      height: $titleHeight;
      border-bottom: 1px solid #999;
      display: flex;
      justify-content: space-between;
      align-items: center;
      .login-title {
        margin-bottom: 0;
        margin-left: 10px;
        font-weight: bold;
        font-size: 1.25rem;
        user-select: none;
        color: #333;
      }
      .btn-exit {
        width: 50px;
        text-align: center;
        color: #666;
        cursor: pointer;
        transition: color .5s ease;
        &:hover {
          color: #000;
        }
      }
    }
    .work-area {
      height: 100%-$titleHeight;
      font-size: 1rem;
      font-weight: bold;
      color: #333;
      padding: 20px;
      form {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px;
        label {
          width: 20%;
          user-select: none;
        }
        input {
          @media screen and(max-width: $wndWidth){
            max-width: 80%;
          }
          border: 1px solid #ccc;
          padding: 3px 5px;
          border-radius: 3px;
          box-shadow: inset 0 1px 2px rgba(0, 0, 0, .075);
          transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
          &:focus {
            border-color: #007bff;
            outline: 0;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, .075), 0 0 4px rgba(102, 175, 233, .6);
          }
        }
      }
      .btns {
        display: flex;
        margin: 30px;
        justify-content: space-around;
        @media screen and(max-width: $wndWidth){
          margin-top: -10px;
        }
      }
    }
  }
</style>
