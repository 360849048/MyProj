<template>
  <Fade>
    <div class="shade" v-show="showWnd" @mousedown.self="bounceWnd">
      <section class="user-info-wnd" ref="userInfoWnd">
        <div class="titlebar">
          <p class="title">用户信息</p>
          <i class="fa fa-times fa-2x btn-exit" aria-hidden="true" @click="hideWnd"></i>
        </div>
        <article class="main-info-area" v-if="!isEditPwd">
          <p class="account-line"><span class="font-weight-bold">账号：</span><span>{{account}}</span>&nbsp;<span v-if="superAuth">(管理员)</span></p>
          <p class="username-line">
            <span class="font-weight-bold">用户名：</span>
            <span v-if="!isEditUsername">
              {{username}}&nbsp;&nbsp;
              <i class="fa fa-pencil pointer" title="修改用户名" aria-hidden="true" @click="isEditUsername=true"></i>
            </span>
            <span class="username-line" v-else>
              <input type="text" class="username-input" v-model="newUsername" :placeholder="username">
              &nbsp;&nbsp;&nbsp;&nbsp;
              <button class="btn btn-sm btn-outline-primary" @click="commitNewUsername">保存</button>&nbsp;
              <button class="btn btn-sm btn-outline-secondary" @click="isEditUsername=false">取消</button>
            </span>
          <p>
            <span class="font-weight-bold">安全：</span>
            <span><button class="btn btn-sm btn-outline-secondary pointer" @click="isEditPwd=true">修改密码</button></span>
          </p>
          <button class="btn btn-outline-secondary btn-exit" @click="userLogout">注销</button>
        </article>
        <article class="edit-pwd-area" v-else>
          <section class="forms-area">
            <form>
              <label class="font-weight-bold" for="oldPwd">旧密码：</label>
              <input type="password" id="oldPwd" v-model="originPwd">
            </form>
            <form>
              <label class="font-weight-bold" for="newPwd">新密码：</label>
              <input type="password" id="newPwd" v-model="newPwd">
              <i v-if="newPwdErr" class="fa fa-exclamation text-danger err-icon" aria-hidden="true"></i>
            </form>
            <form>
              <label class="font-weight-bold" for="newPwdAgain">新密码确认：</label>
              <input type="password" id="newPwdAgain" v-model="newPwdAgain">
              <i v-if="twoNewPwdDiff" class="fa fa-exclamation text-danger err-icon" aria-hidden="true"></i>
            </form>
          </section>
          <div class="btns">
            <button class="btn btn-outline-primary" @click="commitNewPwd">确认</button>
            <button class="btn btn-outline-secondary" @click="isEditPwd=false">取消</button>
          </div>
        </article>
      </section>
    </div>
  </Fade>
</template>

<script>
  import axios from 'axios'
  import { mapState, mapActions } from 'vuex'
  import Fade from '@/common/animation/Fade'


  export default {
    name: "user-wnd",
    components: {
      Fade
    },
    props: {
      showWnd: Boolean
    },
    computed: {
      ...mapState(['superAuth', 'account', 'username']),
      twoNewPwdDiff () {
        return this.newPwd !== this.newPwdAgain;
      }
    },
    data () {
      return {
        newUsername: '',
        isEditUsername: false,
        isEditPwd: false,
        originPwd: '',
        newPwd: '',
        newPwdAgain: '',
        newPwdErr: false
      }
    },
    methods: {
      ...mapActions(['logout', 'modifyUsername']),
      hideWnd () {
        this.$emit('hidewnd');
      },
      userLogout () {
        axios.get('/api/logout').then(res => {
          this.logout();
          this.hideWnd();
        }).catch(e => {
          console.log(e);
        })
      },
      bounceWnd () {
        const bounceTimes = 3;
        const iterval = 100;
        let count = 0;
        let flag = 0;

        let bounceEvent = window.setInterval(() => {
          if (flag === 0) {
            flag = 1;
            this.$refs.userInfoWnd.style.transform = 'scale(1.05)';
          } else {
            flag = 0;
            this.$refs.userInfoWnd.style.transform = 'scale(1)';
            count++;
          }
          if (count >= bounceTimes) {
            window.clearInterval(bounceEvent);
          }
        }, iterval)
      },
      commitNewPwd () {
        if (this.twoNewPwdDiff) {
          this.$message({
            message: '输入的两次新密码不一致',
            type: 'error'
          });
          return;
        }
        if (this.newPwd === '') {
          this.$message({
            message: '新密码不能为空',
            type: 'error'
          });
          this.newPwdErr = true;
          return;
        }
        axios.post('/api/modifypwd', {
          originPwd: this.originPwd,
          newPwd: this.newPwd
        }).then(res => {
          res = res.data;
          if (res.status) {
            this.$message({
              message: res['description'],
              type: 'success'
            });
          } else {
            this.$message({
              message: res['description'],
              type: 'error'
            });
          }
        }).catch(err => {
          console.log(err);
        })
      },
      commitNewUsername () {
        if (this.newUsername === '' || this.newUsername === this.username) {
          this.$message({
            message: "用户名修改成功！",
            type: 'success'
          });
          this.isEditUsername = false;
          return
        }
        axios.get(`/api/modifyusername?newUsername=${this.newUsername}`).then(res => {
          res = res.data;
          this.isEditUsername = false;
          this.$message({
            message: res['description'],
            type: res.status ? 'success' : 'error'
          });
          if (res.status) {
            this.modifyUsername(this.newUsername);
          }
        }).catch(err => {
          console.log(err);
        })
      }
    },
    watch: {
      isEditPwd: {
        handler: function(cv, ov) {
          if (cv) {
            this.$refs.userInfoWnd.style.height = '300px';
          } else {
            this.$refs.userInfoWnd.style.height = '280px';
            this.originPwd = '';
            this.newPwd = '';
            this.newPwdAgain = '';
          }
        }
      },
      isEditUsername (cv) {
        if (!cv) {
          this.newUsername = '';
        }
      },
      newPwd (cv, ov) {
        if (ov === '' && cv !== '') {
          this.newPwdErr = false;
        }
      }
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
    display: flex;
    justify-content: center;
    align-items: center;
    .user-info-wnd {
      $wndWidth: 400px;
      $wndHeight: 280px;
      $titleHeight: 15%;
      width: $wndWidth;
      height: $wndHeight;
      box-shadow: 0 0 20px #666;
      background: #fff;
      border-radius: 5px;
      transition: height ease .3s, transform ease .3s;
      @media screen and(max-width: $wndWidth) {
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
        .title {
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
      .main-info-area {
        margin: 1rem .5rem;
        font-size: 1.1rem;
        p {
          height: 2.25rem;
        }
        .username-line {
          display: flex;
          align-items: center;
          .username-input {
            height: 2rem;
            width: 7rem;
            border: 0;
            border-bottom: 1px solid #ccc !important;
            padding: 3px 10px;
            transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
            &:focus {
              border-color: #007bff;
              outline: 0;
              border-bottom: 1px solid #007BFF !important;
            }
          }
        }
        .btn-exit {
          margin: 0 auto;
          display: block;
          width: 50%;
        }
      }
      .edit-pwd-area {
        font-size: 1.1rem;
        margin: 1.5rem .5rem;
        form {
          display: flex;
          margin: .75rem 1rem;
          align-items: center;
          label {
            width: 30%;
          }
          input {
            width: 60%;
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
          .err-icon {
            margin-left: .5rem;
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
  }
  .pointer {
    cursor: pointer;
  }
</style>
