<template>
    <div id="srcmaker">
      <div class="container">

        <div class="row">
          <div class="col-2"></div>
          <div class="col-10">
            <ul class="nav nav-tabs">
              <li class="nav-item" v-for="eachPage in pages" @click="gotoPage(eachPage)">
                <a class="nav-link" :class="{'active': curPage === eachPage}" href="#">{{eachPage}}</a>
              </li>
            </ul>
          </div>
        </div>

        <div class="row">
          <div class="col-sm-2">
            <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
              <a class="nav-link active" id="v-pills-home-tab" data-toggle="pill" href="#" role="tab">Digital Input</a>
              <a class="nav-link" id="v-pills-profile-tab" data-toggle="pill" href="#" role="tab">Digital Output</a>
              <a class="nav-link" id="v-pills-messages-tab" data-toggle="pill" href="#" role="tab">Analog Input</a>
              <a class="nav-link" id="v-pills-settings-tab" data-toggle="pill" href="#" role="tab">Analog Output</a>
            </div>
          </div>
          <div class="col-sm-5">
            <ul>
              <li v-for="(input, index) in ios" v-if="index < Math.ceil((curPageStartItem + curPageEndItem)/2)">
                <div class="alert alert-primary" role="alert">
                  {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                </div>
              </li>
            </ul>
          </div>
          <div class="col-sm-5">
            <ul>
              <li v-for="(input, index) in ios" v-if="index >= Math.ceil((curPageStartItem + curPageEndItem)/2)">
                <div class="alert alert-primary" role="alert">
                  {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
</template>
<script>

  let pageItemAmount = 32;

  export default {
    data(){
      return {
        ioNum: pageItemAmount,
        ios: {},
        pageItemAmount: pageItemAmount,
        curPage: 1
      }
    },
    computed: {
      pages: function(){
        let pageAmount = Math.ceil( this.ioNum / this.pageItemAmount );
        let pgs = [];
        for(let i=1; i<= pageAmount; i++){
          pgs.push(i);
        }
        return pgs
      },
      curPageStartItem: function(){
        return 1 + (this.curPage - 1) * this.pageItemAmount
      },
      curPageEndItem: function(){
        return this.curPage * this.pageItemAmount < this.ioNum ? this.curPage * this.pageItemAmount : this.ioNum;
      }
    },
    methods: {
      gotoPage(page){
        if (this.pages.indexOf(page) === -1){
          return -1;
        }
        this.curPage = page;

        let _this = this;
        $.ajax({
          url: "/io/di",
          type: 'GET',
          dataType: 'json',
          data: {"start": _this.curPageStartItem, 'end': _this.curPageEndItem},
          success: function(data){
            _this.ioNum = data.amount;
            // json数据内部按key排序，可直接使用
            _this.ios = data.ios;
          },
          error: function(){
            console.log('Error!!!');
            _this.ioNum = 120;
            let temp = {};
            for(let i=_this.curPageStartItem; i<=_this.curPageEndItem; i++){
              temp[i] = i;
            }
            _this.ios = temp;
          }
        });
        return 0;
      }
    },
    mounted() {
      this.gotoPage(this.curPage);
    }
  }
</script>
<style scoped lang='scss'>
  ul{
    list-style-type: none;
  }
  .nav.nav-tabs{
    margin: 10px;
    .nav-item{
      display: inline-block;
      width: 100px;
      text-align: center;
    }
  }
  .alert .badge-light{
    float: right;
  }
  /* Overwrite default bootstrap style */
  .alert{
    width: 80%;
    display: inline-block;
    padding: .15rem 1.25rem;
    margin-bottom: 0.25rem;
  }
</style>
