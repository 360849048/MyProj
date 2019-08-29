<template>
  <div id="nav">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand user-area" href="javascript:">
      <i v-if="!isLogin" class="fa fa-user" aria-hidden="true" @click="popLoginWnd"></i>
      <span v-else @click="popUserInfoWnd">{{username}}</span>
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent" >
      <ul class="navbar-nav mr-auto">
        <li
          class="nav-item"
          :class="{'active': curRoute === 1}"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
            <router-link class="nav-link" href="#" to ="/home" @click.native="curRoute=1">
              <i class="fa fa-home fa-fw"></i>
              Home
            </router-link>
        </li>
        <li
          class="nav-item"
          :class="{'active': curRoute === 2}"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
            <router-link class="nav-link" href="#" to="/versions" @click.native="curRoute=2">
              <i class="fa fa-code-fork" aria-hidden="true"></i>
              Versions
            </router-link>
        </li>
        <li class="nav-item dropdown" :class="{'active': curRoute === 3}">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="fa fa-magic"></i>
              Tools
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <router-link
                class="dropdown-item"
                href="###"
                to="/srctransfer"
                @click.native="curRoute=3"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">
                <i class="fa fa-minus-circle"></i>
                Select
              </router-link>
              <router-link
                class="dropdown-item"
                href="###"
                to="/makeio"
                @click.native="curRoute=3"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">
                <i class="fa fa-files-o"></i>
                IO
              </router-link>
              <router-link
                class="dropdown-item"
                href="###"
                to="/bezier"
                @click.native="curRoute=3"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">
                <i class="fa fa-ils" aria-hidden="true"></i>
                Bezier
              </router-link>
              <div class="dropdown-divider"></div>
              <a
                class="dropdown-item"
                href="###"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">more...</a>
            </div>
        </li>
        <li
          class="nav-item"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
            <a class="nav-link disabled" href="###">Link</a>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"
             v-model="textSearch"
             @keydown.enter.prevent="search">
      <button
        class="btn btn-outline-success my-2 my-sm-0"
        type="button"
        @click="search"
        :data-toggle="clientWidth<=992 ? 'collapse' : ''"
        data-target="#navbarSupportedContent">Search</button>
      </form>
    </div>
    </nav>
    <!-- 登录框 -->
    <Fade>
      <div class="wnd shade" v-if="showLoginWnd" @click.self="hideLoginWnd">
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
              <button class="btn btn-primary" @click="userLogin">确认</button>
              <button class="btn btn-secondary" @click="resetUserInfo">重置</button>
            </div>
          </div>
        </div>
      </div>
    </Fade>
    <Fade>
      <div class="wnd shade" v-if="showUserInfoWnd" @click.self="hideUserInfoWnd">
        <section class="user-info-wnd">
          <h2>用户信息</h2>
          <article>
            <p><span>账号：</span><span>{{account}}</span></p>
            <p v-if="superAuth">管理员权限</p>
          </article>
          <button @click="userLogout">注销</button>
        </section>
      </div>
    </Fade>
  </div>
</template>

<style lang="scss" scoped>
  /* Overwrite default bootstrap style */
  .navbar-toggler {
    &:focus {
      outline: 0;
    }
    &:host {
      display: flex;
    }
    flex: 1;
    border: none !important;
    text-align: right !important;
  }
  @media(max-width: 991px){
    a:hover {
      background-color: #fff;
      border-radius: 5px;
    }
    a.disabled:hover {
      background-color: inherit;
    }
    .dropdown-menu {
      border: none !important;
      background-color: inherit !important;
      max-height: 0;
      transition: max-height .5s ease;
      overflow: hidden;
      display: block !important;
      padding: 0;
    }
    .dropdown-menu.show {
      max-height: 150px;
    }
  }
  .shade {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(100, 100, 100, .5);
  }
  .wnd {
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
    .user-info-wnd {
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
    }
  }
</style>

<script>
  // import md5 from '@/libs/md5'
  import axios from 'axios'
  import Fade from '@/common/animation/Fade'
  import { mapState, mapActions } from 'vuex'

  // 因为babel的处理，直接在Import处解构赋值会失败
  // let {MD5} = md5;

  export default {
    components: {
      Fade
    },
    computed: {
      ...mapState(['isLogin', 'username', 'superAuth'])
    },
    data(){
      return {
        curRoute: 1,
        textSearch: '',
        clientWidth: 0,
        timer: null,
        showLoginWnd: false,
        account: '',
        password: '',
        showUserInfoWnd: false,
      }
    },
    methods: {
      ...mapActions(['login', 'logout']),
      search(){
        this.$router.push({
          path: 'search',
          query:{
            text: this.textSearch
          }
        });
        this.curRoute = 9;
      },
      popLoginWnd () {
        this.showLoginWnd = true;
      },
      hideLoginWnd () {
        this.showLoginWnd = false;
      },
      resetUserInfo () {
        this.account = '';
        this.password = '';
      },
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
            let userInfo = {'username': res.username, 'superAuth': res.sp};
            this.login(userInfo);
            this.$message({
              message: '登录成功',
              type: 'success'
            });
          } else {
            this.$message({
              message: '密码或账号错误',
              type: 'error'
            });
          }
        }).catch(err => {console.log(err)})
      },
      popUserInfoWnd () {
        this.showUserInfoWnd = true;
      },
      hideUserInfoWnd () {
        this.showUserInfoWnd = false;
      },
      userLogout () {
        axios.get('/api/logout').then(res => {
          this.logout();
          this.hideUserInfoWnd()
        }).catch(e => {
          console.log(e);
        })
      }
    },
    mounted () {
      this.clientWidth = document.body.clientWidth;

      let _this = this;
      window.onresize = () => {
        if (_this.timer) {
          clearTimeout(_this.timer);
        }
        _this.timer = setTimeout(()=>{
          _this.clientWidth = document.body.clientWidth;
        }, 50);
      };

      // try {
      //   let username = sessionStorage.getItem("username");
      //   let superAuth = sessionStorage.getItem("superAuth") === "1";
      //   if (username !== null) {
      //     this.login({username, superAuth});
      //   }
      // } catch(e) {
      //   axios.get('/api/logout');
      //   this.logout();
      // }
      axios.get('/api/verifystatus').then(res => {
        res = res.data;
        if (res['status']) {
          this.account = res['account'];
          this.login({'username': res['username'], 'superAuth': res['sp']});
        }
      }).catch(e => {
        console.log(e);
      })
    }
  }
</script>
<style>
  #nav {
    position: relative;
    z-index: 999;
  }
  #nav nav {
    opacity: .97;
  }
  .user-area {
    min-width: 2rem;
  }
  .user-area * {
    display: inline-block;
    width: 100%;
    text-align: center;
  }
</style>
