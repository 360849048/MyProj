<template>
  <Fade>
    <div class="shade" v-show="showWnd" @mousedown.self="bounceWnd">
      <section class="new-note-wnd" ref="newNoteWnd">
        <header class="titlebar">
          <p class="title">新增记录</p>
          <i class="fa fa-times fa-2x btn-exit icon-hover-style" aria-hidden="true" @click="hideWnd"></i>
        </header>
        <div>
          <h3 class="input-wrap">
            <label class="name" for="version">新版本</label>
            <input id="version" class="" type="text" v-model="version">
          </h3>
          <h4 class="input-wrap">
            <label class="name" for="origin">原版本</label>
            <input id="origin" class="" type="text" v-model="origin">
          </h4>
          <ul class="release-notes">
            <li class="release-note-item" v-for="(item, itemId) in releaseNote" :key="itemId">
              <span class="text-danger item-icon">*</span>
              <input type="text" :ref="itemId">
            </li>
          </ul>
          <i class="icon-append fa fa-plus pointer icon-hover-style"
             aria-hidden="true" title="新增一条" @click="appendItem">
          </i>
        </div>
        <footer>
          <button class="btn btn-outline-primary" @click="save">保存</button>
          <button class="btn btn-outline-secondary" @click="reset">取消</button>
        </footer>
      </section>
    </div>
  </Fade>
</template>

<script>
  import Fade from '@/common/animation/Fade'


  export default {
    name: "new-note-wnd",
    components: {
      Fade
    },
    props: {
      showWnd: Boolean
    },
    computed: {
    },
    data () {
      return {
        version: "",
        origin: "",
        releaseNote: ['',],
      }
    },
    methods: {
      hideWnd () {
        this.$emit('hidewnd');
      },
      bounceWnd () {
        const bounceTimes = 3;
        const iterval = 100;
        let count = 0;
        let flag = 0;

        let bounceEvent = window.setInterval(() => {
          if (flag === 0) {
            flag = 1;
            this.$refs.newNoteWnd.style.transform = 'scale(1.05)';
          } else {
            flag = 0;
            this.$refs.newNoteWnd.style.transform = 'scale(1)';
            count++;
          }
          if (count >= bounceTimes) {
            window.clearInterval(bounceEvent);
          }
        }, iterval)
      },
      appendItem () {
        this.releaseNote.push('');
      },
      save () {
        for (let i=0; i<this.releaseNote.length; i++) {
          this.releaseNote[i] = this.$refs[i][0].value;
        }
        this.$emit('notecommit', {version: this.version, origin: this.origin, releaseNote: JSON.parse(JSON.stringify(this.releaseNote))});
        this.reset();
      },
      reset () {
        this.hideWnd();
        this.version = "";
        this.origin = "";
        this.releaseNote.splice(0, this.releaseNote.length, '');
        this.$refs['0'][0].value = '';
      }
    },
  }
</script>

<style scoped lang="scss">
  .shade {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 100;
    background-color: rgba(100, 100, 100, .5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .new-note-wnd {
    $wndWidth: 800px;
    $wndHeight: 680px;
    $titleHeight: 3rem;
    width: $wndWidth;
    // height: $wndHeight;
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
      }
    }
    .input-wrap {
      margin-top: .5rem;
      padding: 0 1.5rem;
      display: flex;
      align-items: center;
      .name {
        width: 7rem;
      }
      input {
        width: 50%;
      }
    }
    .release-notes {
      margin: 1rem 3rem;
      .release-note-item {
        display: flex;
        input {
          width: 100%;
        }
      }
    }
    .icon-append {
      margin: 0 2.75rem;
    }
    footer {
      padding: 2rem 10rem;
      display: flex;
      justify-content: space-around;
      align-items: center;
    }
  }
  .pointer {
    cursor: pointer;
  }
  .icon-hover-style {
    color: #666;
    cursor: pointer;
    transition: color .5s ease;
    &:hover {
      color: #000;
    }
  }
  input {
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
</style>
