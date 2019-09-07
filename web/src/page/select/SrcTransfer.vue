<template>
  <div id="srctransfer">
    <div class="container">
      <div class="row justify-content-around">
        <div class="col-md-5" id="imm-type">
          <imm-type
                    @changeType="getType"
                    @changeLock="getLock"
                    @changeInject="getInject"
                    @changeStandard="getStandard">
          </imm-type>
        </div>
      </div>

      <label for="random_codes">5级随机码</label>
      <input id="random_codes" type="text" v-model="randomCodes"  @keydown.enter="getPwd5">
      <button class="btn btn-primary" @click="getPwd5">获取5级密码</button>

  </div>
    <textarea name="文本编辑" id="text-edit" cols="50" rows="10">
      <h1>新版本V05_46_00</h1>
      <h2>原版本V05_45_00</h2>
      KEB参数导入导出
      增加F6Blue程序（头文件编译，第三位功能码为3时是F6Blue、为2是F6Gray）
      F6Blue 寻零、自整定需要打开抱闸，即写7，15的步骤，写32775,32783
      F6Blue 上马达时，延时需要延长1.5s
      F6Blue顶出抱闸检测更改
      修改全自动、半自动按开合模按钮，可编程中子和顶退异常的问题
      修改中子时间模式下，中子压力流量偶尔不会输出的问题
      增加冷却时建压的功能
      可编程中子增加动作中止和顺序中止
      可编程中子压力流量自动情况无法修改
      捷克语、德语更新
      仿真模式完善
      F6Blue编码器跳动大，导致储料轴的standstill一直0,1变化
    </textarea>
  </div>
</template>
<script>
  import axios from 'axios'
  import ImmType from './components/ImmType'

  export default{
    components:{
      ImmType,
    },
    data(){
      return{
        immParams: {
          type: '',
          lock: '',
          inject: '',
          standard: ''
        },
        ios: {di1: '可编程io输入1', do1: '可编程io输出1'},
        module: 'cdm163',
        randomCodes: '',
      }
    },
    methods: {
      getType(type){
        this.immParams.type = type;
      },
      getLock(lock){
        this.immParams.lock = lock;
      },
      getInject(inject){
        this.immParams.inject = inject;
      },
      getStandard(standard){
        this.immParams.standard = standard;
      },
      getPwd5 () {
        if (this.randomCodes.search(/\d{10}$/) !== 0) {
          alert("5级随机码长度必须是10，且都是0-9的数字");
          return;
        }
        axios.get(`/api/getpwd5?randomcodes=${this.randomCodes}`).then(res => {
          res = res.data;
          console.log(res);
          alert('5级密码为: ' + res);
        }).catch(e => {
          console.log(e);
        })
      }
    }
  }
</script>
<style lang="scss" scoped>
  #imm-type{
    user-select: none;
  }
  #imm-params{
    // height: 150px;
  }
</style>
