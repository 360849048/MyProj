<template>
  <div id="home"  v-loading="loading">
    <header><h1 class="ml-2">标准程序更新记录</h1></header>
    <!-- 侧边导航栏 -->
    <nav class="side-nav">
      <ul>
        <li
          class="side-nav-item"
          v-for="(ver, verId) in verInfo" :key="verId"
          @click="scrollTo(verId)"
        >
          {{ver.version}}
          <span class="text-secondary" v-show="edMode[verId]">*</span>
        </li>
      </ul>
      <div class="slider-bar" ref="sliderBar"></div>
    </nav>
    <aside class="side-func-bar">
      <a class="pointer hover-primary" @click="addNewReleaseNote">
        <i class="fa fa-plus" aria-hidden="true"></i>
        &nbsp;新增
      </a>
      <new-note-wnd
        :showWnd="showNewNoteWnd"
        @notecommit="getNewNote"
        @hidewnd="showNewNoteWnd=!showNewNoteWnd">
      </new-note-wnd>
    </aside>
    <main>
       <!--Release Note主体-->
      <section v-for="(ver, verId) in verInfo" :key="verId">
        <article class="ver-wrap" :ref="verId">
          <h3 class="title main-title">
            <span>新版本</span>
            <span v-if="!edMode[verId]">{{ver.version}}</span>
            <input class="edit-mode" v-else type="text" :value="ver.version">
          </h3>
          <h4 class="title sub-title">
            <span>原版本</span>
            <span v-if="!edMode[verId]">{{ver.origin}}</span>
            <input class="edit-mode" v-else type="text" :value="ver.origin">
          </h4>
          <div>
            <ul>
              <li class="release-note-item" v-for="(item, itemId) in ver.releaseNote" :key="itemId">
                <span class="text-danger item-icon">*</span>
                <span v-if="!edMode[verId]" class="ml-2">{{item}}</span>
                <input class="edit-mode" v-else type="text" :value="item">
              </li>
            </ul>
          </div>
          <i class="icon-edit fa fa-edit" v-show="!edMode[verId]" aria-hidden="true" title="编辑" @click="toggleEditMode(verId)"></i>
          <i class="icon-save fa fa-check" v-show="edMode[verId]" aria-hidden="true" title="保存" @click="saveChange(verId)"></i>
          <i class="icon-cancel fa fa-close" v-show="edMode[verId]" aria-hidden="true" title="取消" @click="resetChange(verId)"></i>
          <i class="icon-append fa fa-plus" v-show="edMode[verId]" aria-hidden="true" title="新增一行" @click="appendItem(verId)"></i>
          <i class="icon-delete fa fa-trash" v-show="edMode[verId]" aria-hidden="true" title="删除该记录" @click="deleteNote(verId)"></i>
        </article>
        <a class='line-next' v-if="verId < verNum"></a>
      </section>
    </main>
    <footer>
      <p>Services Powered By Python 3.4.1</p>
      <p>Vue.js</p>
    </footer>
  </div>
</template>

<script>
  import tools from '@/libs/tool.js'
  import axios from 'axios'
  import { mapState } from 'vuex'
  import NewNoteWnd from './components/NewNoteWnd'

  const scroll = tools.scroll;

  export default{
    components: {NewNoteWnd},
    computed: {
      ...mapState(['superAuth']),
      verNum () {
        let verIds = Object.keys(this.verInfo);
        return verIds.length;
      }
    },
    data() {
      return {
        verInfo: {},
        verInfoOrigin: {},
        innerTimer: null,
        loading: true,
        edMode: {},
        showNewNoteWnd: false
      }
    },
    methods: {
      pullReleaseNote () {
        axios.get('/api/ver/releasenote').then(res => {
          res = res.data;
          if (res.status) {
            this.verInfo = JSON.parse(JSON.stringify(res['releaseNote']));
            this.verInfoOrigin = JSON.parse(JSON.stringify(res['releaseNote']));
            for (let key in this.verInfo) {
              this.$set(this.edMode, key, false);
            }
          } else {
            this.verInfo = {};
            this.verInfoOrigin = {};
          }
          this.loading = false;
        }).catch(err => {
          console.log(err);
          this.loading = false;
        })
      },
      scrollTo (id) {
        let domArticle = this.$refs[id][0];
        let domSliderBar = this.$refs.sliderBar;

        scroll(domArticle.offsetTop, 500);
        domSliderBar.style.top = 1.75 * (id - 1) + 'rem';
      },
      innerScrollEvent () {
        if (this.innerTimer) {
          window.clearTimeout(this.innerTimer);
        }
        this.innerTimer = window.setTimeout(() => {
          // article元素内容的向下偏移补偿
          const offset = 250;
          let actScrollPos = document.documentElement.scrollTop;
          let scrollHeight = document.documentElement.scrollHeight;
          let clientHeight = document.documentElement.clientHeight;
          let verItemTop;

          if (actScrollPos + clientHeight >= scrollHeight) {
          // 滚动到底部
            this.$refs.sliderBar.style.top = (this.verNum - 1) * 1.75 + 'rem';
            return;
          }

          for (let verId in this.verInfo) {
            verItemTop = this.$refs[verId][0].offsetTop;

            if (verItemTop + offset >= actScrollPos) {
              this.$refs.sliderBar.style.top = (verId - 1) * 1.75 + 'rem';
              break;
            }
          }
        }, 50);
      },
      toggleEditMode (verId) {
        this.edMode[verId] = !this.edMode[verId];
      },
      saveChange (verId) {
        if (!this.superAuth) {
          this.$message({
            message: '请先登录后再保存',
            type: 'warning'
          });
          return;
        }
        let version = this.$refs[verId][0].querySelector(".main-title input").value;
        let origin = this.$refs[verId][0].querySelector(".sub-title input").value;
        let releaseNoteArr = [];
        let domNotes = this.$refs[verId][0].querySelectorAll(".release-note-item input");
        let domNoteKeys = Object.keys(domNotes);
        for(let i=0; i<domNoteKeys.length; i++) {
          // js遍历数组别用for in
          if (domNotes[domNoteKeys[i]].value !== '') {
            // 删除空的更改项
            releaseNoteArr.push(domNotes[domNoteKeys[i]].value);
          }
        }
        this.verInfo[verId].version = version;
        this.verInfo[verId].origin = origin;
        this.verInfo[verId].releaseNote = releaseNoteArr;

        axios.post('/api/version/modifyreleasenote', {
          id: this.verInfo[verId].id,
          version: version,
          origin: origin,
          releaseNote: releaseNoteArr
        }).then(res => {
          res = res.data;
          if (res.status) {
            this.verInfoOrigin = JSON.parse(JSON.stringify(this.verInfo));
            this.$message({
              message: '保存成功',
              type: 'success'
            });
            this.edMode[verId] = !this.edMode[verId];
          } else {
            this.$message({
              message: res["description"],
              type: 'error'
            });
            this.resetChange(verId);
          }
        }).catch(err => {
          console.log(err);
        });
      },
      resetChange (verId) {
        this.$refs[verId][0].querySelector(".main-title input").value = this.verInfo[verId].version;
        this.$refs[verId][0].querySelector(".sub-title input").value = this.verInfo[verId].origin;

        let domNotes = this.$refs[verId][0].querySelectorAll(".release-note-item input");
        let domNoteKeys = Object.keys(domNotes);
        for(let i=0; i<domNoteKeys.length; i++) {
          // js遍历数组别用for in
          domNotes[domNoteKeys[i]].value = this.verInfo[verId].releaseNote[i];
        }
        this.verInfo = JSON.parse(JSON.stringify(this.verInfoOrigin));
        this.edMode[verId] = !this.edMode[verId];
      },
      appendItem (verId) {
        // 操作verInfo会导致视图重新渲染，因为input未进行v-model绑定，
        // 会导致原先编辑的文本丢失，所以需要先保存之前的状态
        let version = this.$refs[verId][0].querySelector(".main-title input").value;
        let origin = this.$refs[verId][0].querySelector(".sub-title input").value;
        let releaseNoteArr = [];
        let domNotes = this.$refs[verId][0].querySelectorAll(".release-note-item input");
        let domNoteKeys = Object.keys(domNotes);
        for(let i=0; i<domNoteKeys.length; i++) {
          releaseNoteArr.push(domNotes[domNoteKeys[i]].value);
        }
        this.verInfo[verId].version = version;
        this.verInfo[verId].origin = origin;
        this.verInfo[verId].releaseNote = releaseNoteArr;

        // 将input中的value保存到verInfo中，才可进行verInfo操作
        this.verInfo[verId]['releaseNote'].push('');
      },
      addNewReleaseNote () {
        if (!this.superAuth) {
          this.$message({
            message: '请先登录',
            type: 'warning'
          });
          return;
        }
        this.showNewNoteWnd = true;
      },
      getNewNote (e) {
        if (!this.superAuth) {
          this.$message({
            message: '请先登录后再提交',
            type: 'warning'
          });
          return;
        }
        axios.post('/api/version/newnote', {
          version: e.version,
          origin: e.origin,
          releaseNote: e.releaseNote
        }).then(res => {
          res = res.data;
          if (res.status) {
            this.$message({
              message: '添加成功',
              type: 'success'
            });
            this.pullReleaseNote();
          } else {
            this.$message({
              message: res['description'],
              type: 'error'
            });
          }
        }).catch(err => {
          console.error(err);
        })
      },
      deleteNote (verId) {
        if (!this.superAuth) {
          this.$message({
            message: '请先登录后操作',
            type: 'warning'
          });
          return;
        }
        axios.post("/api/version/delnote", {
          id: this.verInfo[verId]['id']
        }).then(res => {
          res = res.data;
          if (res.status) {
            delete this.verInfo[verId];
            delete this.verInfoOrigin[verId];
            this.$message({
              message: '删除成功',
              type: 'success'
            });
            this.pullReleaseNote();
          } else {
            this.$message({
              message: res['description'],
              type: 'error'
            });
          }
        }).catch (err => {
          console.error(err);
        })
      }
    },
    mounted () {
      this.pullReleaseNote();

    },
    activated () {
      // bind会返回一个新的函数，
      // 为了能够在deactivated中成功解绑scroll事件，
      // 将bind返回的新方法添加到window属性中
      window.homeScrollEventListner = this.innerScrollEvent.bind(this);
      document.addEventListener("scroll", window.homeScrollEventListner);
    },
    deactivated () {
      document.removeEventListener("scroll", window.homeScrollEventListner);
    },
    watch: {}
  }
</script>

<style scoped lang="scss">
  $bgc: #fcfcfc;
  $maxPageWidth: 1400px;
  * {
    padding: 0;
    margin: 0;
    word-wrap: break-word;
  }
  ul {
    list-style: none;
  }
  a {
    text-decoration: none;
    color: inherit;
  }
  .pointer {
    cursor: pointer;
  }
  .hover-primary:hover {
    color: #007bff !important;
  }
  #home {
    background-color: $bgc;
    position: absolute;
    left: 0;
    right: 0;
    top: 56px;
  }
  main {
    max-width: $maxPageWidth;
    margin: 0 auto;
    .ver-wrap {
      margin: 4rem 10rem;
      padding: 1rem;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 4px 3px 8px 0 #e4e4e4;
      position: relative;
      .title {
        display: flex;
        /*white-space: nowrap;*/
        &.main-title {
          text-indent: .25rem;
          // height: 33px;
          input.edit-mode {
            height: 32px;
          }
        }
        &.sub-title {
          text-indent: 1rem;
          // height: 28px;
          input.edit-mode {
            height: 22px;
          }
        }
        margin: .5rem;
        input.edit-mode {
          border: 0;
          border-bottom: 1px solid #ccc !important;
          width: 100%;
          padding: 3px 8px;
          transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
          &:focus {
            border-color: #007bff;
            outline: 0;
            border-bottom: 1px solid #007BFF !important;
          }
        }
      }
      .release-note-item {
        margin: .5rem 1.5rem;
        display: flex;
        .item-icon {
          user-select: none;
        }
        input.edit-mode {
          height: 1.5rem;
          width: 100%;
          border: 0;
          border-bottom: 1px solid #ccc !important;
          padding: 3px 8px;
          transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s;
          &:focus {
            border-color: #007bff;
            outline: 0;
            border-bottom: 1px solid #007BFF !important;
          }
        }
      }
      .icon-save, .icon-cancel, .icon-edit, .icon-delete {
        position: absolute;
        top: .75rem;
        cursor: pointer;
      }
      .icon-edit  {
        display: none;
      }
      &:hover>.icon-edit {
        display: inline;
      }
      .icon-cancel {
        right: 4rem;
      }
      .icon-save, .icon-edit {
        right: 1rem;
      }
      .icon-delete {
        right: 7rem;
      }
      .icon-append {
        cursor: pointer;
        position: absolute;
        bottom: .25rem;
        left: 2.2rem;
      }
    }
  }
  .side-nav {
    position: fixed;
    left: 10px;
    top: 120px;
    bottom: 100px;
    z-index: 10;
    overflow-y: scroll;
    padding-right: 1rem;
    background-color: $bgc;
    &::-webkit-scrollbar{
      width: 6px;
      height: 6px;
    }
    &::-webkit-scrollbar-thumb{
      border-radius: 10px;
      -webkit-box-shadow: inset 0 0 5px rgba(0,0,0,0.2);
      background: #818080;
    }
    ul{
      position: relative;
      .side-nav-item {
        cursor: pointer;
        margin: 0 .25rem .25rem;
        font-weight: bold;
        box-sizing: border-box;
        line-height: 1.5rem;
        height: 1.5rem;
        color: #666;
        &:hover {
          border-bottom: 1px solid #ccc
        }
      }
    }
    .slider-bar {
      background-color: #21f3c0;
      width: 6rem;
      height: 1.5em;
      position: absolute;
      top: 0;
      right: 0;
      left: 0;
      z-index: -1;
      box-shadow: 6px 5px 8px #e0e0e0;
      border-radius: 5px;
      transition: top .5s ease;
    }
  }
  .side-func-bar {
    position: absolute;
    top: 60px;
    right: 30px;
  }
  .line-next {
    position: relative;
    text-align: center;
    display: block;
    background-color: rgba(0, 0, 0, 0);
    &::after {
      content: 'Next';
      display: inline;
      padding: 0 .5rem;
      background-color: $bgc;
      position: relative;
    }
    &::before {
      content: '';
      display: block;
      border-bottom: 1px solid #ccc;
      margin: 0 5rem;
      position: absolute;
      z-index: 0;
      left: 0;
      right: 0;
      top: 50%;
    }
  }
  footer {
    border-top: 1px solid #ccc;
    height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
