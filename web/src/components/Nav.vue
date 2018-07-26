<template>
  <div id="#nav">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">TEST</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
            <router-link class="nav-link" href="#" to="/home"><i class="fa fa-home fa-fw"></i>Home <span class="sr-only">(current)</span></router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link" href="#" to="/versions">Versions</router-link>
        </li>
        <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Tools
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <router-link class="dropdown-item" href="#" to="/srctransfer">Select</router-link>
            <router-link class="dropdown-item" href="#" to="/io">IO</router-link>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="#">more...</a>
            </div>
        </li>
        <li class="nav-item">
            <a class="nav-link disabled" href="#">Link</a>
        </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" v-model="textSearch">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
    </div>
    </nav>
  </div>
</template>
<script>
export default {
    data(){
        return {
            textSearch: ''
        }
    }
}
</script>
