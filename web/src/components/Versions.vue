<template>
  <div id="versions">
    <!-- 导航栏（更新按钮、版本切换卡） -->
    <div>
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a class="nav-link disabled" style="user-select: none">Software-versions&nbsp;
            <i class="fa fa-refresh" :class="{'fa-spin': updating}" aria-hidden="true" @click="checkUpdateInfo" style="cursor: pointer"></i>
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
                </div>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- 底部页码 -->
    <footer class="fixed-bottom">
      <div id="pagination">
        <el-pagination
          layout="prev, pager, next"
          :total="itemsNum * 10 / pageItemAmount"
          :current-page="curPage"
          @current-change="gotoPage">
        </el-pagination>
      </div>
    </footer>
    <!-- 更新确认框 -->
    <div class="modal fade" id="updateInfoCheckdialog" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">检查到<b class="text-danger">{{softType}}</b>有下列更新</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <ul v-if="versReadyToUpdate.length > 0">
              <li v-for="ver in versReadyToUpdate">{{ver[0]}} {{ver[1]}} {{ver[7]}}</li>
            </ul>
            <p v-else>已经是最新！</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="startUpdate">确认更新</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  /**
   * 数据处理逻辑:
   * 1.常量pageItemAmount规定一页最多显示的数据，
   * 2.通过ajax的get方式从后台按需获取当页所需要的数据，并非一次性全部得到所有数据。
   *  第一次ajax请求某类软件版本时数据量按pageItemAmount来（服务器允许请求数据超过实际服务器数据库容量），
   *
   */

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
        pageItemAmount: pageItemAmount,
        versReadyToUpdate: [],
        curPage: 1
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
            _this.$message({
              showClose: true,
              message: '网络连接失败，无法获取数据',
              type: 'error'
            });
            console.log('AJAX请求无法获取Version列表');
            _this.softVers = {
              1: {
                client: 'Zhafir',
                version: 'V0X_38_50',
                date: '2018.08.18',
                base: 'V0X_38_20',
                record: '新增较多功能',
                reason: '这是一个例子',
                remark: '',
                author: 'XX',
                path: 'G:/windows/system32/test.rar'
              },
              2: {
                client: 'test1',
                version: 'V0X_15_XX',
                date: '2017.01.18',
                base: 'V0X_15_15',
                record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
                reason: '这也是一个例子',
                remark: '',
                author: '员工A',
                path: ''
              },
              3: {
                client: 'test2',
                version: 'V0X_15_XX',
                date: '2017.01.18',
                base: 'V0X_15_15',
                record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
                reason: '这还是一个例子',
                remark: '',
                author: '技术员B',
                path: ''
              },
              4: {
                client: 'test3',
                version: 'V0X_15_XX',
                date: '2017.01.18',
                base: 'V0X_15_15',
                record: '1.一组吹气 2.一组气动中子 3.一组阀门 4.两组模温监控 5.质量参数公差设定质量监控画面的监控值 6.质量监控画面增加：模温异常的不良判定 7.质量判别控制电气接口，传送带 8.一组可编程I/O 9.下料口温度闭环控制 10.调模模式下打开后安全门，蜂鸣器不响 1.产品质量监控对循环周期只采样一次',
                reason: '这依旧是一个例子',
                remark: '',
                author: '管理人员C',
                path: 'g:/sigmatek/测试/v0x-15-xx.rar;g:/临时/管理人员C/v0x_15_xx.7z'
              },
            };
          }
        });
      },
      gotoPage(e){
        this.curPage = parseInt(e);
        let firstSeq = (this.curPage - 1) * pageItemAmount;
        let lastSeq = this.curPage * pageItemAmount;
        this.getVers(firstSeq, lastSeq);
      },
      checkUpdateInfo(){
        let _this = this;
        $.ajax({
          url: "/checkupdate",
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
              $('#updateInfoCheckdialog').modal('show');
              _this.versReadyToUpdate = data.newVers;
            }else{
              _this.$message({
                showClose: true,
                message: data.description,
                type: 'error'
              });
            }
          },
          error: function(){
            _this.$message({
              showClose: true,
              message: '网络无法连接，更新失败',
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
      startUpdate(){
        let _this = this;
        $.ajax({
          url: "/startupdate",
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
                message: '更新成功',
                type: 'success'
              });
              // 更新后刷新页面
              _this.gotoPage(1);
              _this.versReadyToUpdate = [];
            }else{
              _this.$message({
                showClose: true,
                message: data.description,
                type: 'error'
              });
            }
          },
          error: function(){
            _this.$message({
              showClose: true,
              message: '网络无法连接，更新失败',
              type: 'error'
            });
          }
        });
        $('#updateInfoCheckdialog').modal('hide');
      }
    },
    mounted(){
      this.getVers(0, pageItemAmount);
    },
    watch: {
      softType: {
        handler(cval, oval){
          if(cval !== oval){
            this.curPage = 1;
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
    padding-bottom: 5rem;
  }
  .no-bt{
    border-top: 0;
  }
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
