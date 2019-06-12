<template>
  <div class="container" v-loading="loading">
    <section class="item" v-for="(section, sectionIdx) in ioSections">
      <div class="title">{{sectionIdx}}</div>
      <ul class="main">
        <li class="line"
          v-for="(io, ioIdx) in section"
          @dragover.prevent=""
          @drop="dropIo"
          :data-index="ioIdx"
        >
          <span class="io-index"
                :class="{'badge-success': ioType === 'DI',
                'badge-danger': ioType === 'DO',
                'badge-info': ioType === 'AI' || ioType === 'TI',
                'badge-warning': ioType === 'AO' || ioType === 'TO'}"
                :data-index="ioIdx"
          >
            {{ioIdx}}
          </span>
          <div
            class="alert alert-primary io-name"
            :class="[checkChanged(ioIdx) ? 'alert-danger' : 'alert-primary']"
            role="alert"
            v-if="io"
            @dblclick="dblclickIo(ioIdx)"
            :data-index="ioIdx"
          >
            {{io}}
          </div>
          <div
            class="alert alert-primary io-name opacity02"
            v-else-if="getIoBefore(ioIdx)"
            :data-index="ioIdx"
          >
            {{getIoBefore(ioIdx)}}
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>

  const LINE_ITEM_AMOUNT = 16;

  export default {
    name: "base-io",
    props: {
      ioType: String,
      stdIo: Object,
      originStdIo: Object,
      loading: Boolean,
      allIO: Object,
    },
    computed: {
      ios () {
        // ios: {1: "编码器调模A", 2: "调模编码器B",...}
        let _ios = {};
        let io_seq;
        for (let i=1; i<=this.stdIo[this.ioType].length; i++) {
          io_seq = this.stdIo[this.ioType][i - 1];
          if (io_seq === 0) {
            // 该位置未配置IO
            _ios[i] = '';
          } else {
            _ios[i] = this.allIO[this.ioType][io_seq - 1];
          }
        }
        return _ios;
      },
      ioSections () {
        // ioSections: {1: {1: "编码器调模A", 2: "调模编码器B", ...}, 2: {17: "", ...}, 3: {...}...}
        let ioSection = {};
        let idx;
        for (let i in this.ios) {
          idx = Math.ceil(i / LINE_ITEM_AMOUNT);
          if (!ioSection[idx]) {
            ioSection[idx] = {};
          }
          ioSection[idx][i] = this.ios[i];
        }
        return ioSection;
      },
    },
    methods: {
      dblclickIo (ioIdx) {
        let newStdIoConfig = JSON.parse(JSON.stringify(this.stdIo[this.ioType]));

        try {
          newStdIoConfig[ioIdx - 1] = 0;
        } catch (e) {
          alert('StdIo删除IO错误');
          console.log(e);
        }
        this.$emit('stdioupdate', newStdIoConfig);
      },
      dropIo (e) {
        let newStdIoConfig = JSON.parse(JSON.stringify(this.stdIo[this.ioType]));
        // 获取并解析drag-drop事件传递过来的数据
        let ioInfo = e.dataTransfer.getData('ioInfo');
        let [fromIoType, item] = ioInfo.split('--');
        item = parseInt(item);
        let stdIoIdx = e.target.getAttribute('data-index');

        if (fromIoType !== this.ioType || this.stdIo[this.ioType][stdIoIdx - 1] !== 0) {
          // IO类型不相同，或已经被占用，不允许配置
          console.log('from: ', fromIoType, item, 'to: ', this.ioType, this.stdIo[this.ioType][stdIoIdx - 1]);
          return;
        }
        newStdIoConfig[stdIoIdx - 1] = item;
        this.$emit('stdioupdate', newStdIoConfig);
      },
      checkChanged (idx) {
        return this.stdIo[this.ioType][idx - 1] !== this.originStdIo[this.ioType][idx - 1]
      },
      getIoBefore (idx) {
        return this.allIO[this.ioType][this.originStdIo[this.ioType][idx - 1] - 1];
      },
    }
  }
</script>

<style scoped lang="scss">
  ul {
    list-style: none;
  }
  .container {
    /*border: dashed 1px lightpink;*/
    display: flex;
    flex-wrap: wrap;
    .item {
      width: 33.3%;
      padding: 10px;
      /*background-color: #eee;*/
      .title {
        background-color: rgba(240, 240, 240, .8);
        line-height: 30px;
        border-radius: 5px;
      }
      .main {
        .line {
          width: 100%;
          border-bottom: 1px red dotted;
          height: 35px;
          display: flex;
          align-items: center;
          .io-index {
            width: 20px;
            height: 20px;
            margin-right: 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 10px;
            flex-shrink: 0;
            user-select: none;
          }
          .io-name {
            width: 100%;
            padding: .15rem 1rem;
            user-select: none;
            margin-bottom: 0 !important;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            &:hover {
              overflow: visible;
            }
          }
        }
      }
    }
    @media (max-width: 992px) {
      .item {
        width: 50%;
      }
    }
    .opacity02 {
      opacity: .2;
    }
  }
</style>
