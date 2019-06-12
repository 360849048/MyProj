<template>
  <div id="funcSwitch">
    <div class="container-fluid">
      <div class="show-inline">
        <button type="button" class="btn btn-lg"
                :class="[status ? 'btn-outline-success' : 'btn-outline-danger']"
                @click="toggleStatus">
          <i class="fa" :class="[status ? 'fa-check' : 'fa-times']" aria-hidden="true"></i>&nbsp;&nbsp;{{status | toChinese}}
        </button>
        <div class="name">{{name}}</div>
        <el-popover
          placement="right"
          width="200"
          trigger="hover"
          v-if="desc !== ''"
          :content="desc">
          <i class="fa fa fa-question icon-style" slot="reference"></i>
        </el-popover>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "func-switch",
    props: ['id', 'name', 'status', 'desc'],
    filters: {
      toChinese(input){
        return input ? '开' : '关';
      }
    },
    methods: {
      toggleStatus(){
        this.$emit('statusupdate', {id: this.id, status: !this.status});
      }
    }
  }
</script>

<style scoped>
  #funcSwitch{
    /*border: 1px dotted gray;*/
    display: flex;
    align-items: center;
  }
  button{
    width: 5rem !important;
  }
  .name{
    font-size: 1.7rem;
    margin-left: 1rem;
  }
  .show-inline {
    display: flex;
    justify-content: flex-start;
  }
  .icon-style {
    user-select: none;
    cursor: pointer;
    color: #ccc;
    opacity: .5;
    transition-property: opacity,color;
    transition-duration: .5s;
  }
  .icon-style:hover {
    color: #666;
    opacity: 1;
  }
</style>
