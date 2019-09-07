<template>
  <div id="home"  v-loading="loading">
    <header><h1 class="ml-2">标准程序更新记录</h1></header>
    <main>
      <!-- 侧边导航栏 -->
      <nav class="side-nav">
        <ul>
          <li
            class="side-nav-item"
            v-for="(ver, verId) in verInfo" :key="verId"
            @click="scrollTo(verId)"
          >
            {{ver.version}}
          </li>
        </ul>
        <div class="slider-bar" ref="sliderBar"></div>
      </nav>
      <!-- Release Note主体 -->
      <section v-for="(ver, verId) in verInfo" :key="verId">
        <article class="ver-wrap" :ref="verId">
          <div class="title main-title h3">新版本
            <span v-if="!edMode[verId]">{{ver.version}}</span>
            <input class="edit-mode" v-else type="text" :value="ver.version">
          </div>
          <div class="title sub-title h4">原版本
            <span v-if="!edMode[verId]">{{ver.origin}}</span>
            <input class="edit-mode" v-else type="text" :value="ver.origin">
          </div>
          <div>
            <ul>
              <li class="release-note-item" v-for="(item, itemId) in ver.releaseNote" :key="itemId">
                <span class="text-danger item-icon">*</span>
                <span v-if="!edMode[verId]" class="ml-2">{{item}}</span>
                <input class="edit-mode"  v-else type="text" :value="item">
              </li>
            </ul>
            </div>
          <i class="icon-edit fa fa-edit" aria-hidden="true" title="编辑" @click="toggleEditMode(verId)"></i>
          <button class="btn btn-primary" v-if="edMode[verId]" @click="saveChange(verId)">保存</button>
        </article>
        <a class='line-next' v-if="verId < verNum"></a>
      </section>
    </main>
    <footer>
      <p>End</p>
      <p>Services Powered By Python 3.4.1</p>
      <p>Vue.js</p>
    </footer>
  </div>
</template>

<script>
  import tools from '@/libs/tool.js'
  import axios from 'axios'

  const scroll = tools.scroll;

  export default{
    computed: {
      verNum () {
        let verIds = Object.keys(this.verInfo);
        return verIds.length;
      }
    },
    data() {
      return {
        verInfo: {},
        innerTimer: null,
        loading: true,
        edMode: {},
      }
    },
    methods: {
      pullReleaseNote () {
        axios.get('/api/ver/releasenote').then(res => {
          res = res.data;
          if (res.status) {
            this.verInfo = res['releaseNote'];
            for (let key in this.verInfo) {
              this.$set(this.edMode, key, false);
            }
          } else {
            this.verInfo = {};
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
        let version = this.$refs[verId][0].querySelector(".main-title input").value;
        let origin = this.$refs[verId][0].querySelector(".sub-title input").value;
        let releaseNoteArr = [];
        let domNotes = this.$refs[verId][0].querySelectorAll(".release-note-item input");
        let domNoteKeys = Object.keys(domNotes);
        for(let i=0; i<domNoteKeys.length; i++) {
          // js遍历数组别用for in
          releaseNoteArr.push( domNotes[domNoteKeys[i]].value);
        }
        console.log(version, origin, releaseNoteArr);
        this.verInfo[verId].version = version;
        this.verInfo[verId].origin = origin;
        this.verInfo[verId].releaseNote = releaseNoteArr;
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
        .main-title {
          text-indent: .25rem;
        }
        .sub-title {
          text-indent: 1rem;
        }
        margin: .5rem;
        .edit-mode {
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

      .release-note-item {
        margin: .5rem 1.5rem;
        display: flex;
        .item-icon {
          user-select: none;
        }
        .edit-mode {
          height: 2rem;
          width: 100%;
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
      .icon-edit {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
        display: none;
      }
      &:hover>.icon-edit {
        display: inline;
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
    text-align: center;
    justify-content: center;
    align-items: center;
  }
</style>
