<template>
    <div id="searchResult">
      <h1 v-if="isSerachMode">This is a page to show Search Result</h1>
      <h1 v-else>This is a page to show Version Reference</h1>
      <h3 v-if="isSerachMode">你搜索的关键字为：<span class="text-danger font-weight-bold">{{ajaxMsg}}</span>&nbsp;(多个关键字请用空格隔开)</h3>
      <h3 v-else>这里展示的是<span class="text-danger font-weight-bold">{{ajaxMsg}}</span>相关软件版本</h3>
      <!-- 软件版本显示区域 -->
      <div style="clear: both;">
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
            <tr v-for="(msg, index) in softVers" :key="index" :class="{'text-warning': msg.version === ajaxMsg}">
              <td scope="col"><div class="in-one-line">{{msg.client}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.version}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.date}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.base}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.record}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.reason}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.remark}}</div></td>
              <td scope="col"><div class="in-one-line">{{msg.author}}</div></td>
              <td scope="col">
                <div class="dropright">
                  <i class="fa fa-bolt pointer" :class="{'text-danger': hasPath(msg)}" aria-hidden="true" aria-haspopup="true" aria-expanded="false"
                     data-toggle="dropdown">
                  </i>
                  <div class="dropdown-menu">
                    <template v-if="hasPath(msg)">
                      <a href="javascript:" class="dropdown-item" v-for="item in msg.path.split(';')"
                         @click="downloadSrcCode(item)">
                        <i class="fa fa-download" aria-hidden="true"></i>
                        {{item}}&nbsp;
                      </a>
                      <div class="dropdown-divider"></div>
                      <a class="dropdown-item" href="javascript:" v-if="msg.torefresh == 1">
                        <i class="fa fa-exclamation"></i>
                        该路径已被举报，注意文件可靠性
                      </a>
                      <div class="dropdown-divider" v-if="msg.torefresh == 1"></div>
                    </template>
                    <template>
                      <a class="dropdown-item" href="javascript:" @click="searchReference(msg.version)">
                        显示该版本相关其他版本
                      </a>
                    </template>
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
  import axios from 'axios'

  export default {
    name: "search-result",
    computed: {
      isSerachMode () {
        return this.$route.query.text !== undefined;
      }
    },
    data(){
      return{
        loading: false,
        ajaxMsg: 'ok',
        softVers: {},
        curPage: 1
      }
    },
    methods: {
      searchVers(_this) {
        $.ajax({
          url: '/api/ver/searchversions',
          data: {text: _this.ajaxMsg},
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
          url: '/api/ver/downloadsrccode',
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
      referVers () {
        this.loading = true;
        axios.get(`/api/ver/referversions?ver=${this.ajaxMsg}`).then(res => {
          res = res.data;
          this.loading = false;
          this.softVers = res.items;
        } ).catch( e => {
          console.log(e);
          this.loading = false;
        })
      },
      searchReference (version) {
        this.$router.push({
          path: 'search',
          query: {
            ver: version
          }
        })
      },
      hasPath (msg) {
        return msg.path !== '' && msg.path !== null;
      },
    },
    watch:{
      '$route'(to, from){
        if (this.isSerachMode) {
          this.ajaxMsg = this.$route.query.text;
          this.searchVers(this);
        } else {
          this.ajaxMsg = this.$route.query.ver;
          this.referVers();
        }
      }
    },
    mounted(){
      // 初次进入该组件时候，并不会触发$route的更改，所以需要在这里处理
      if (this.isSerachMode) {
        this.ajaxMsg = this.$route.query.text;
        this.searchVers(this);
      } else {
        this.ajaxMsg = this.$route.query.ver;
        this.referVers();
      }
    },
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
