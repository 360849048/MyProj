<template>
    <div id="searchResult">
      <div style="clear: both;">
        <!-- 进行全盘检索时显示的内容 -->
        <section v-if="showDiskSearchPage">
          <hr>
          <section>
            <ul>
              <li class="back-end-searching-item" v-for="(searchItem, searchId) in diskSearchBackEndInfo" :key="searchId">
                <div>
                  <p><span class="font-weight-bold">关键字：</span>{{searchItem["key"]}}</p>
                  <p><span class="font-weight-bold">开始时间：</span>{{searchItem["starting_time"]}}</p>
                  <p><span class="font-weight-bold">状态：</span><span v-if="searchItem['status']">已完成</span><span v-else>正在进行</span></p>
                  <p><span class="font-weight-bold">模式：</span><span v-if="searchItem['mode'] == 0">普通</span><span v-else>正则</span></p>
                  <button class="btn btn-outline-primary" @click="switchToLookDiskSearch(searchId)">查看此搜索</button>
                </div>
              </li>
            </ul>
          </section>
          <section class="search-input-wrap">
            <!--<label for="disk-search-input" class="search-icon"><i class="fa fa-search fa-2x" aria-hidden="true"></i></label>-->
            <input id="disk-search-input" type="search" aria-label="Search" v-model="ajaxMsg">
            <button class="disk-search-btn pointer" @click="startDiskSearch">开始</button>
          </section>
          <section class="search-config text-center">
            <span class="mr-2 font-weight-bold">查找模式：</span>
            <input type="radio" id="normal-mode" name="search-mode" v-model="diskSearchMode" value="0"><label for="normal-mode" class="mr-2">普通模式</label>
            <input type="radio" id="regex-mode" name="search-mode" v-model="diskSearchMode" value="1"><label for="regex-mode" class="mr-2">正则模式</label>
          </section>
          <h5><i class="fa fa-warning text-warning"></i>
            注意：在磁盘中搜索文件会消耗很多时间及服务器资源，搜索的实时结果将在下面显示
          </h5>
          <h6 v-if="diskSearchStatus === 2">搜索完成，共遍历文件 {{diskSearchFileNum}}，得到结果 {{diskSearchResult.length}}</h6>
          <div v-else-if="diskSearchStatus === 1">
            <h6>正在搜索，已遍历文件 {{diskSearchFileNum}}</h6>
            <button class="btn btn-danger" @click="terminateDiskSearch">终止搜索</button>
          </div>
          <ul class="mt-5 ml-5">
            <li v-for="(item, index) in diskSearchResult" :key="index">{{item}}</li>
          </ul>
        </section>
        <!-- 显示在数据库中搜索得到的版本内容以及版本之间的关联信息 -->
        <section class="col-12" v-else-if="Object.keys(softVers).length !== 0 | loading">
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
              <td scope="col"><div class="in-one-line" :class="{'text-danger': hasPath(msg), 'font-weight-bold': hasPath(msg)}">{{msg.version}}</div></td>
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
        </section>
        <!-- 版本数据库中没有找到任何信息时，显示下面页面 -->
        <section v-else>
          <hr>
          <h4 class="text-center"><i class="fa fa-warning text-warning"></i>
            没有在版本数据库中搜索到相应版本，请尝试更新版本库后重试或
            <span class="pointer text-danger" @click="showDiskSearchPage = true">全盘搜索</span>
          </h4>
        </section>
      </div>
    </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "search-result",
    computed: {
      isSerachMode() {
        return this.$route.query.text !== undefined;
      }
    },
    data() {
      return {
        loading: false,
        ajaxMsg: '',
        softVers: {},
        curPage: 1,
        showDiskSearchPage: false,
        progressFetchTimer: null,
        diskSearchResult: {},
        diskSearchFileNum: 0,
        diskSearchStatus: 0,
        diskSearchMode: 0,
        diskSearchId: '',
        diskSearchBackEndInfo: {},
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
      downloadSrcCode(path) {
        let _this = this;
        $.ajax({
          type: 'GET',
          url: '/api/ver/downloadsrccode',
          dataType: 'json',
          data: {'path': path},
          beforeSend: function () {

          },
          success: function (data) {
            if (data.status.toUpperCase() === 'SUCCESS' && data.url) {
              window.open(data.url);
            } else {
              alert('后台遇到错误，无法下载文件，错误描述: ' + data.description);
            }
          },
          error: function (xhr, type) {
            _this.waiting = false;
            alert('无法连接服务器');
          }
        })
      },
      referVers() {
        this.loading = true;
        axios.get(`/api/ver/referversions?ver=${this.ajaxMsg}`).then(res => {
          res = res.data;
          this.loading = false;
          this.softVers = res.items;
        }).catch(e => {
          console.log(e);
          this.loading = false;
        })
      },
      searchReference(version) {
        this.$router.push({
          path: 'search',
          query: {
            ver: version
          }
        })
      },
      hasPath(msg) {
        return msg.path !== '' && msg.path !== null;
      },
      startDiskSearch () {
        this.diskSearchResult = [];
        this.diskSearchFileNum = 0;
        let diskSearchId = '';
        // get请求无法正确传输'+'等特殊字符，只能用post
        axios.post('/api/ver/startdisksearch', {
          key: this.ajaxMsg,
          mode: this.diskSearchMode
        }).then(res => {
          res = res.data;
          this.switchToLookDiskSearch(res.id);
        }).catch(e => {
          console.log(e);
        });
      },
      terminateDiskSearch () {
        axios.get(`/api/ver/stopdisksearchthread?id=${this.diskSearchId}`).then(res => {
          res = res.data;
          if (!res.status) {
            alert("停止失败！");
          }
        })
      },
      switchToLookDiskSearch (searchId) {
        window.clearInterval(this.progressFetchTimer);
        this.diskSearchId = searchId;
        this.diskSearchStatus = 1;
        this.progressFetchTimer = window.setInterval(() => {
          axios.get(`/api/ver/getdisksearchprogress?id=${this.diskSearchId}`).then(res => {
            res = res.data;
            this.diskSearchResult = res["progress"];
            this.diskSearchFileNum = res["num"];
            if (res.status) {
              this.diskSearchStatus = 2;
              window.clearInterval(this.progressFetchTimer);
            }
          })
        }, 1000);
      }
    },
    watch: {
      '$route'(to, from) {
        window.clearInterval(this.progressFetchTimer);
        if (this.isSerachMode) {
          this.ajaxMsg = this.$route.query.text;
          this.showDiskSearchPage = false;
          if (this.ajaxMsg !== '') {
            this.searchVers(this);
          }
        } else {
          this.ajaxMsg = this.$route.query.ver;
          this.showDiskSearchPage = false;
          if (this.ajaxMsg !== '') {
            this.referVers();
          }
        }
      }
    },
    destroyed () {
      window.clearInterval(this.progressFetchTimer);
    },
    mounted() {
      // 初次进入该组件时候，并不会触发$route的更改，所以需要在这里处理
      if (this.isSerachMode) {
        this.ajaxMsg = this.$route.query.text;
        if (this.ajaxMsg !== '') {
          this.searchVers(this);
        }
      } else {
        this.ajaxMsg = this.$route.query.ver;
        if (this.ajaxMsg !== '') {
          this.referVers();
        }
      }
      // 检查当前后台是否在进行全盘搜索
      axios.get("/api/ver/getdisksearchthreads").then(res => {
        res = res.data;
        this.diskSearchBackEndInfo = res;
      })
    },
  }
</script>

<style scoped lang="scss">
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
  .search-input-wrap {
    position: relative;
    width: 50%;
    margin: 0 auto;
    label {
      position: absolute;
      left: .75rem;
      top: .5rem;
    }
    input {
      width: 100%;
      height: 3rem;
      font-size: 1.5rem;
      border: 1px solid #3385ff;
      padding: .25rem 6.5rem .25rem .5rem;
      /*border-radius: 1.5rem;*/
      box-shadow: inset 0 1px 2px rgba(0, 0, 0, .075);
      transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
      &:focus {
        border-color: #007bff;
        outline: 0;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, .075), 0 0 4px rgba(102, 175, 233, .6);
      }
    }
    button {
      position: absolute;
      right: 0;
      top: 0;
      height: 3rem;
      border: 0;
      width: 6rem;
      background-color: #3385ff;
      color: #fff;
      font-size: 1.25rem;
      box-shadow: inset 0 1px 2px rgba(0, 0, 0, .075), 0 0 4px #ddd;
      &:hover {
        background-color: #317ef3
      }
      &:active {
        background-color: #3075dc;
      }
    }
  }
  .back-end-searching-item {
    display: inline-block;
    margin: 1rem;
    padding: 1rem;
    border: 1px solid gray;
    border-radius: 5px;
  }
</style>
