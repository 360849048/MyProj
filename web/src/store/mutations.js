export default {
  login (state, userInfo) {
    state.isLogin = true;
    state.username = userInfo.username;
    state.superAuth = userInfo.superAuth;
    // try {
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
  }
}
