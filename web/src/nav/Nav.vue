<template>
  <div id="nav">
    <nav
      class="navbar navbar-expand-lg navbar-light bg-light"
      :class="{ 'green-style': curRoute === 4}"
    >
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
          :class="{'active': curRoute === 4}"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
          <router-link class="nav-link" href="#" to="/log" @click.native="curRoute=4">
            <i class="fa fa-list-alt" aria-hidden="true"></i>
            Log
          </router-link>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
        <section class="search-wrap">
          <label for="search-input" class="search-icon"><i class="fa fa-search" aria-hidden="true"></i></label>
          <input class="form-control mr-sm-2" id="search-input" type="search" aria-label="Search"
                 v-model="textSearch"
                 @keydown.enter.prevent="search">
        </section>
        <button
          class="btn btn-outline-success my-2 my-sm-0"
          type="button"
          @click="search"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">Search</button>
      </form>
    </div>
    </nav>
    <!-- 登录 -->
    <login-wnd :showWnd="showLoginWnd" @hidewnd="hideLoginWnd"></login-wnd>
    <!-- 用户信息 -->
    <user-wnd :showWnd="showUserInfoWnd" @hidewnd="hideUserInfoWnd"></user-wnd>
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
  .green-style {
    ::selection {
      background:#d3d3d3;
      color:#555;
    }
    background: #1b926c !important;
    color: #c7e7dc;
    .dropdown-menu {
      background: #1b926c !important;
    }
    * {
      color: #c7e7dc !important;
    }
    a:hover {
      background: #1fa67a !important;
    }
    input {
      color: #333 !important;
      background-color: #c7e7dc;
      transition: background-color .5s ease;
      &:focus {
        background-color: #eee;
      }
    }
    .search-icon * {
      color: #666 !important;
    }
    .active *{
      color: #fff !important;
    }
  }
  .search-wrap {
    position: relative;
    .search-icon {
      position: absolute;
      left: 10px;
      top: 10px;
    }
    #search-input {
      padding-left: 40px;
    }
  }
</style>

<script>
  // import md5 from '@/libs/md5'
  import axios from 'axios'
  import Fade from '@/common/animation/Fade'
  import LoginWnd from './components/LoginWnd'
  import UserWnd from './components/UserWnd'
  import { mapState, mapActions } from 'vuex'

  // 因为babel的处理，直接在Import处解构赋值会失败
  // let {MD5} = md5;

  export default {
    components: {
      Fade,
      LoginWnd,
      UserWnd,
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
      popUserInfoWnd () {
        this.showUserInfoWnd = true;
      },
      hideUserInfoWnd () {
        this.showUserInfoWnd = false;
      },
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
          this.login({'account': res['account'], 'username': res['username'], 'superAuth': res['sp']});
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
    transition: .5s ease;
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
