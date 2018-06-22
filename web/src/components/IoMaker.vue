<template>
    <div id="srcmaker">
      <div class="container">
        <div class="row">
          <div class="col-sm">
            <ul>
              <li v-for="(input, index) in inputs" v-if="index <= Math.ceil(Object.keys(inputs).length/2)">
                <div class="alert alert-primary" role="alert">
                  {{index}}&nbsp;&nbsp;&nbsp;{{input}}
                </div>
              </li>
            </ul>
          </div>
          <div class="col-sm">
            <ul>
              <li v-for="(input, index) in inputs" v-if="index > Math.ceil(Object.keys(inputs).length/2)">
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
  export default {
    data(){
      return {
        inputs: {
          "1": "电动门开",
          "2": "电动门关",
          "3": 'xxx',
          "4": 'xxxx',
          "5": 'xxxxx'
        }
      }
    },
    mounted() {
      // console.log("需要从服务器获取标准io列表");
      console.log($.ajax({
        url: "/foo",
        type: 'GET',
        data: this.immParams,
        dataType: 'json',
        success: function(data){
          console.log(data);
        },
        error: function(){
          console.log('Error!!!');
        }
      }));
    }
  }
</script>
<style scoped>
  ul{
    list-style-type: none;
  }
  .alert{
    width: 80%;
    display: inline-block;
  }
</style>
