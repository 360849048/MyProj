<template>
  <div id="#nav">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="###">NEW!</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent" >
      <ul class="navbar-nav mr-auto">
        <li
          class="nav-item"
          :class="{'active': curRoute === 1}"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
            <router-link class="nav-link" href="#" to ="/home" @click.native="curRoute=1">
              <i class="fa fa-home fa-fw"></i>
              Home
            </router-link>
        </li>
        <li
          class="nav-item"
          :class="{'active': curRoute === 2}"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
            <router-link class="nav-link" href="#" to="/versions" @click.native="curRoute=2">
              <i class="fa fa-code-fork" aria-hidden="true"></i>
              Versions
            </router-link>
        </li>
        <li class="nav-item dropdown" :class="{'active': curRoute === 3}">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="fa fa-magic"></i>
              Tools
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
              <router-link
                class="dropdown-item"
                href="###"
                to="/srctransfer"
                @click.native="curRoute=3"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">
                <i class="fa fa-minus-circle"></i>
                Select
              </router-link>
              <router-link
                class="dropdown-item"
                href="###"
                to="/makeio"
                @click.native="curRoute=3"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">
                <i class="fa fa-files-o"></i>
                IO
              </router-link>
              <router-link
                class="dropdown-item"
                href="###"
                to="/bezier"
                @click.native="curRoute=3"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">
                <i class="fa fa-ils" aria-hidden="true"></i>
                Bezier
              </router-link>
              <div class="dropdown-divider"></div>
              <a
                class="dropdown-item"
                href="###"
                :data-toggle="clientWidth<=992 ? 'collapse' : ''"
                data-target="#navbarSupportedContent">more...</a>
            </div>
        </li>
        <li
          class="nav-item"
          :data-toggle="clientWidth<=992 ? 'collapse' : ''"
          data-target="#navbarSupportedContent">
            <a class="nav-link disabled" href="###">Link</a>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"
             v-model="textSearch"
             @keydown.enter.prevent="search">
      <button
        class="btn btn-outline-success my-2 my-sm-0"
        type="button"
        @click="search"
        :data-toggle="clientWidth<=992 ? 'collapse' : ''"
        data-target="#navbarSupportedContent">Search</button>
      </form>
    </div>
    </nav>
  </div>
</template>

<style lang="scss" scoped>
  /* Overwrite default bootstrap style */
  .navbar-toggler {
    &:focus {
      outline: 0;
    }
    &:host {
      display: flex;
    }
    flex: 1;
    border: none !important;
    text-align: right !important;
  }
  @media(max-width: 991px){
    a:hover {
      background-color: #fff;
      border-radius: 5px;
    }
    a.disabled:hover {
      background-color: inherit;
    }
    .dropdown-menu {
      border: none !important;
      background-color: inherit !important;
      max-height: 0;
      transition: max-height .5s ease;
      overflow: hidden;
      display: block !important;
      padding: 0;
    }
    .dropdown-menu.show {
      max-height: 150px;
    }
  }
</style>

<script>
export default {
  data(){
    return {
      curRoute: 1,
      textSearch: '',
      clientWidth: 0,
      timer: null,
    }
  },
  methods: {
    search(){
      this.$router.push({
        path: 'search',
        query:{
          text: this.textSearch
        }
      });
      this.curRoute = 9;
    }
  },
  mounted () {
    this.clientWidth = document.body.clientWidth;

    let _this = this;
    window.onresize = () => {
      if (_this.timer) {
        clearTimeout(_this.timer);
      }
      _this.timer = setTimeout(()=>{
        _this.clientWidth = document.body.clientWidth;
      }, 50);
    }
  }
}
</script>
