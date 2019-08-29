export default {
  login (ctx, userInfo) {
    ctx.commit('login', userInfo);
  },
  logout (ctx) {
    ctx.commit('logout');
  }
}
