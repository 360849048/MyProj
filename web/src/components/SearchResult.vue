<template>
    <div id="searchResult">
      <h1>This is a page to show Search Result</h1>
      <h3>你搜索的关键字为：<span class="text-danger font-weight-bold">{{msg}}</span>&nbsp;(多个关键字请用空格隔开)</h3>
      <!-- 软件版本显示区域 -->
      <div class="row" style="clear: both;">
        <div class="col-12">
          <table class="table table-hover" v-loading="loading">
            <thead>
            <tr>
              <th scope="col" class="no-bt">客户</th>
              <th scope="col" class="no-bt">版本</th>
              <th scope="col" class="no-bt">更改日期</th>
              <th scope="col" class="no-bt">原版本</th>
              <th scope="col" class="no-bt">内容</th>
              <th scope="col" class="no-bt">原因</th>
              <th scope="col" class="no-bt">备注</th>
              <th scope="col" class="no-bt">更改人</th>
              <th scope="col" class="no-bt">更多</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(msg, index) in softVers" :key="index">
              <td scope="col"><div class="in-one-line">{{msg.client}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.version}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.date}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.base}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.record}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.reason}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.remark}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.author}}</div></td>
              <td scope="col">
                <div class="dropright" v-show="msg.path !== ''">
                  <i class="fa fa-bolt text-danger pointer" aria-hidden="true" aria-haspopup="true" aria-expanded="false"
                     data-toggle="dropdown">
                  </i>
                  <div class="dropdown-menu">
                    <a href="##" class="dropdown-item" v-for="item in msg.path.split(';')"
                       @click="downloadSrcCode(item)">
                      {{item}}&nbsp;
                      <i class="fa fa-download" aria-hidden="true"></i>
                    </a>
                  </div>
                </div>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
</template>

<script>
  // 定义每页最多显示的信息条数
  const pageItemAmount = 30;

  export default {
    name: "search-result",
    data(){
      return{
        loading: false,
        msg: 'ok',
        softVers: {},
        curPage: 1
      }
    },
    methods: {
      searchVers(_this) {
        $.ajax({
          url: 'searchversions',
          data: {text: _this.msg},
          type: 'GET',
          dataType: 'json',
          beforeSend: function () {
            _this.loading = true;
          },
          complete: function () {
            _this.loading = false;
          },
          success: function (data) {
            _this.softVers = data.items;
          },
          error: function () {
            _this.$message({
              showClose: true,
              message: '网络连接失败，无法获取数据',
              type: 'error'
            });
          }
        });
      }
    },
    watch:{
      '$route'(to, from){
        this.msg = to.query.text;
        this.searchVers(this);
      }
    },
    mounted(){
      // 初次进入该组件时候，并不会触发$route的更改，所以需要在这里处理
      this.msg = this.$route.query.text;
      this.searchVers(this);
    }
  }
</script>

<style scoped>
  .pointer{
    cursor: pointer;
  }
</style>
