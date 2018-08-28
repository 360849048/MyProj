<template>
  <div id="versions">
    <div>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link disabled" style="user-select: none">Software-versions&nbsp;
            <i class="fa fa-refresh" :class="{'fa-spin': updating}" aria-hidden="true" @click="updateVers" style="cursor: pointer"></i>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{'active': softType === 'V01'}" href="##" @click="softType='V01'">V01</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{'active': softType === 'V02'}" href="##" @click="softType='V02'">V02</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{'active': softType === 'V03V04'}" href="##" @click="softType='V03V04'">V03V04</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{'active': softType === 'V05'}" href="##" @click="softType='V05'">V05</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{'active': softType === 'T05'}" href="##" @click="softType='T05'">T05</a>
        </li>
      </ul>
    </div>
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
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <footer class="fixed-bottom">
      <div id="pagination">
        <el-pagination
          layout="prev, pager, next"
          :total="itemsNum * 10 / pageItemAmount"
          @current-change="gotoPage">
        </el-pagination>
      </div>
    </footer>
  </div>
</template>
<script>

  // 定义每页最多显示的信息条数
  const pageItemAmount = 30;

  export default{
    name: 'versions',
    data(){
      return{
        loading: false,
        updating: false,
        softVers: {},
        softType: 'V05',
        itemsNum: pageItemAmount,
        pageItemAmount: pageItemAmount
      }
    },
    methods: {
      getVers(firstSeq, lastSeq){
        let _this = this;
        $.ajax({
          url: "/queryversions",
          type: 'GET',
          dataType: 'json',
          data: {"softType": _this.softType, "start": firstSeq, 'end': lastSeq},
          beforeSend: function(){
            _this.loading = true;
          },
          complete: function() {
            _this.loading = false;
          },
          success: function(data){
            _this.itemsNum = data.itemsNum;
            _this.softVers = data.items;
          },
          error: function(){
            console.log('AJAX请求无法获取Version列表');
            _this.softVers = {
              1: {
                client: 'Zhafir',
                version: 'V0X_38_50',
                date: '2018.08.18',
                base: 'V0X_38_20',
                record: '新增较多功能',
                reason: '标准程序',
                remark: '',
                author: 'XX'
              },
              2: {
                client: 'test1',
                version: 'V0X_15_XX',
                date: '2017.01.18',
                base: 'V0X_15_15',
                record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
                reason: '合同',
                remark: '',
                author: '员工A'
              },
              3: {
                client: 'test2',
                version: 'V0X_15_XX',
                date: '2017.01.18',
                base: 'V0X_15_15',
                record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
                reason: '合同',
                remark: '',
                author: '技术员B'
              },
              4: {
                client: 'test3',
                version: 'V0X_15_XX',
                date: '2017.01.18',
                base: 'V0X_15_15',
                record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
                reason: '合同',
                remark: '',
                author: '管理人员C'
              },
            };
          }
        });
      },
      gotoPage(e){
        let firstSeq = (parseInt(e) - 1) * pageItemAmount;
        let lastSeq = parseInt(e) * pageItemAmount;
        this.getVers(firstSeq, lastSeq);
      },
      updateVers(){
        let _this = this;
        $.ajax({
          url: "/updateversions",
          type: 'GET',
          dataType: 'json',
          data: {"softType": _this.softType},
          beforeSend: function(){
            _this.updating = true;
          },
          complete: function(){
            _this.updating = false;
          },
          success: function(data){
            if(data.status.toUpperCase() === 'SUCCESS'){
              _this.$message({
                showClose: true,
                message: '更新成功，细节请见F12控制台',
                type: 'success'
              });
              // 更新后刷新页面
              _this.gotoPage(1);
            }else{
              _this.$message({
                showClose: true,
                message: '无法找到xls软件版本登记文件，更新失败',
                type: 'error'
              });
            }
            
            console.log(data);
          },
          error: function(){
            _this.$message({
              showClose: true,
              message: '网络无法连接，更新失败',
              type: 'error'
            });
          }
        })
      }
    },
    mounted(){
      this.getVers(0, pageItemAmount);
    },
    watch: {
      softType: {
        handler(cval, oval){
          if(cval !== oval){
            this.gotoPage(1);
          }
        }
      }
    }
  }
</script>
<style scoped>
  #versions{
    margin-top: 10px;
    padding-bottom: 2rem;
  }
  .no-bt{
    border-top: 0;
  }
  .in-one-line{
    max-height: 1.5rem;
    overflow: hidden;
    /*text-overflow: ellipsis;*/
    /*white-space: nowrap;*/
    max-width: 1000px;
    transition: .5s max-height;
  }
  @media screen and (max-width: 1200px){
    .in-one-line{
      max-width: 800px !important;
      transition: .5s max-height;
    }
  }
  @media screen and (max-width: 900px){
    .in-one-line{
      max-width: 400px !important;
      transition: .5s max-height;
    }
  }
  tr:hover .in-one-line{
    white-space: normal;
    max-height: 10rem;
    transition: .5s max-height;
  }
  footer{
    background-color: #fff;
    opacity: .5;
    transform: scale(1.5);
    transition: .5s all;
  }
  footer:hover{
    opacity: .9;
    transition: .5s all;
  }
  #pagination{
    display: flex;
    justify-content: center;
  }
</style>
