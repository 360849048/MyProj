export default {
  login (state, userInfo) {
    state.isLogin = true;
    state.account = userInfo.account;
    state.username = userInfo.username;
    state.superAuth = userInfo.superAuth;
    // try {
    // // 使用sesstionStorage在客户端存储登录信息，但是关闭浏览器就失效
    //   sessionStorage.setItem("username", userInfo.username);
    //   if(userInfo.superAuth){
    //     sessionStorage.setItem('superAuth', '1');
    //   } else {
    //     sessionStorage.setItem('superAuth', '0');
    //   }
    // } catch(e) {
    //   console.log(e, "当前浏览器sessionStorage被禁用！")
    // }
  },
  logout (state) {
    state.isLogin = false;
    state.username = undefined;
    state.superAuth = false;
    // try {
    //   sessionStorage.removeItem("username");
    //   sessionStorage.removeItem("superAuth");
    // } catch(e) {
    //   console.log(e, "当前浏览器sessionStorage被禁用！")
    // }
  },
  modifyUsername (state, newUsername) {
    state.username = newUsername;
  }
}
