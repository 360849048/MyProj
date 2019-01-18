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
              <th scope="col" class="no-bt" width="10%">客户</th>
              <th scope="col" class="no-bt" width="7%">版本</th>
              <th scope="col" class="no-bt" width="6%">更改日期</th>
              <th scope="col" class="no-bt" width="7%">原版本</th>
              <th scope="col" class="no-bt" width="45%">内容</th>
              <th scope="col" class="no-bt" width="5%">原因</th>
              <th scope="col" class="no-bt" width="5%">备注</th>
              <th scope="col" class="no-bt" width="10%">更改人</th>
              <th scope="col" class="no-bt" width="5%">更多</th>
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
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item" href="###" v-if="msg.torefresh != 1" @click="submitError(softType, msg.id)">
                      路径信息有误，向后台反馈
                      <i class="fa fa-hand-paper-o"></i>
                    </a>
                    <a class="dropdown-item" v-else>
                      该路径已被举报，注意文件可靠性
                      <i class="fa fa-exclamation"></i>
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
      },
      downloadSrcCode(path){
        let _this = this;
        $.ajax({
          type: 'GET',
          url: '/downloadsrccode',
          dataType: 'json',
          data: {'path': path},
          beforeSend: function(){

          },
          success: function(data){
            if (data.status.toUpperCase() === 'SUCCESS' && data.url){
              window.open(data.url);
            }else{
              alert('后台遇到错误，无法下载文件，错误描述: ' + data.description);
            }
          },
          error: function (xhr, type) {
            _this.waiting = false;
            alert('无法连接服务器');
          }
        })
      },
      submitError (type, id) {
        axios.get(`/submiterror?type=${type}&id=${id}`)
          .then((res) => {
            res = res.data;
            console.log(res);
            this.$message({
              message: '信息提交成功！请等待后台处理',
              type: 'success'
            })
          })
          .catch((err) => {
            console.log(err);
            this.$message({
              showClose: true,
              message: '网络请求发送失败，无法提交信息',
              type: 'error'
            });
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
  .in-one-line{
    max-height: 1.5rem;
    overflow: hidden;
    /*text-overflow: ellipsis;*/
    /*white-space: nowrap;*/
    /*max-width: 1000px;*/
    transition: .5s max-height;
  }
  @media screen and (max-width: 1000px){
    .in-one-line{
      max-height: 3rem;
      transition: .5s max-height;
    }
  }
  tr:hover .in-one-line{
    white-space: normal;
    max-height: 40rem;
    transition: .5s max-height;
  }
</style>
