<!-- src/components/Home.vue -->
<!-- <script>
export default{
    mounted(){this.logout();},
    methods:{
         logout(){
      localStorage.removeItem('token')
      this.$router.push('/')
    }
    }
    }

</script> -->
<script>
export default{
    mounted(){this.logout();},
    methods:{
         logout(){
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('userid')
      this.$router.push('/')
    }}}




</script>
<template>
  <div class="text-center px-3">
    <h1 class="display-5 mb-4">
      This is the place to Park<br>
      Discover the parking space for your<br>
      4‑wheeler parking — available only for 4‑wheelers
    </h1>

    <router-link to="/login"   class="btn btn-success me-2">Login</router-link>
    <router-link to="/register" class="btn btn-success">Register</router-link>
  </div>
</template>

<style scoped>
/* make sure it doesn’t push footer off screen on small content */
:host {
  width: 100%;
}
</style>
