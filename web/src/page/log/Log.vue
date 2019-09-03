<template>
  <div id="log" class="green-style">
    <header>
      <h1>用户操作日志</h1>
      <h3 v-if="!superAuth">登录才有权限访问该资源！</h3>
    </header>
    <section ref="dispArea">
      <article class="wrap-log" v-if="superAuth">
        <ul>
          <li v-for="(item, id) in records"><span class="text-danger font-weight-bold">**&nbsp</span>{{item}}</li>
        </ul>
      </article>
    </section>
    <footer>
      <p>颜色来源：Font Awesome中文网</p>
    </footer>
  </div>
</template>

<script>
  import axios from 'axios'
  import { mapState } from 'vuex'


  export default {
    name: "log",
    computed: {
      ...mapState(['superAuth']),
    },
    data () {
      return {
        records: [],
      }
    },
    methods: {
      getAllLog () {
          axios.get('/api/log/userall').then(res => {
          res = res.data;
          console.log(res);
          if (res.status) {
            this.records = res['list'];
          }
        }).catch(err => {
          console.log(err);
        })
      }
    },
    watch: {
      superAuth: {
        handler: function () {
          this.getAllLog();
        },
        immediate: true
      }
    }
  }
</script>

<style scoped lang="scss">
  * {
    margin: 0;
    padding: 0;
  }
  .green-style {
    $mainBgc: #1fa67a;
    ::selection {
      background:#d3d3d3;
      color:#555;
    }
    header {
      background: $mainBgc;
      color: #fff;
      h1 {
        text-shadow: 4px 3px 0 #1d9d74, 9px 8px 0 rgba(0,0,0,0.15);
      }
    }
    section {
      background-color: #eee;
      &::before {
        content: '';
        display: block;
        width: 100%;
        height: 8rem;
        background: $mainBgc;
      }
    }
    footer {
      background: $mainBgc;
      color: #fff;
    }
  }
  header {
    h1 {
      padding: 1rem 4rem;
      margin: 0;
    }
    h3 {
      padding: .5rem 8rem;
    }
  }
  section {
    /*min-height: 1000px;*/
    /*outline: 1px red solid;*/
  }
  footer {
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  ul {
    list-style: none;
  }
  .wrap-log {
    margin: 0 8rem;
    padding: 1rem;
    background-color: #fff;
    border-radius: 1rem;
    transform: translateY(-4rem);
    box-shadow: 3px 3px 10px 2px #aaa;
  }
</style>
