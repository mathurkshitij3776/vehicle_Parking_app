<!-- <!-- <template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
</template> -->

<!-- <template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">VehicleParking</router-link>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin-dashboard">Admin</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template> --> 
<!-- src/components/Navbar.vue -->

<script>


export default {
  data(){
    return{
      token: "",
      role:""
    }
  },
  mounted(){
      this.loadtoken()
      

  },

  watch:{
        '$route'(to, from){
          this.loadtoken();
        }

  },
  computed:{
    homeroute(){
    if (this.token){   
         if (this.role != 'user'){
         
             return '/AdminDashboard'
         
             }
         
            else{
         
             return '/UserDashboard'
         
             }
          }
          else{
            return '/'
          }
}
  },
 
  methods:{
    loadtoken(){
        this.token = localStorage.getItem('token')
        this.role = localStorage.getItem('role')
    },
    logout(){
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('userid');
      this.$router.push('/')

    }
  }
}
</script>
<template>

  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <h3 v-if="token" style="padding-right: 27px;">Welcome {{ role }}</h3> 
      <router-link class="navbar-brand" to="/" >VehicleParking</router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navMenu"
        aria-controls="navMenu"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navMenu">
        <ul class="navbar-nav ms-auto">
          
          <li class="nav-item">
            <router-link class="nav-link" :to="homeroute">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login" v-if="!token">Login</router-link>
          </li>
          <li class="nav-item">
            <button class="nav-link" @click="logout" v-if="token">Logout</button>
          </li>
          <!-- <li class="nav-item">
            <button class="nav-link" @click="logout" v-if="token">summary</button>
          </li> -->
          <li class="nav-item">
            <router-link class="nav-link" to="/register" v-if="!token">Register</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/searchusers" v-if="role ==='admin'">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/Chart" v-if="token">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/AdminDashboard" v-if="role==='admin'">Admin</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/adminsearch" v-if="role==='admin'">Search</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* ensure it sits above content if needed */
.navbar {
  z-index: 1000;
}
</style>

