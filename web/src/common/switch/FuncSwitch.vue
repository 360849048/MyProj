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
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "func-switch",
    props: ['id', 'name', 'status'],
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
</style>
