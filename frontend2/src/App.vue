<script setup>

// import Foot from './components/Foot.vue';
import Navbar from './components/Navbar.vue';
import Foot from './components/Foot.vue';
// import HelloWorld from './components/HelloWorld.vue'
</script>
<template>
     <Navbar />
  <main style="text-align: center;"> 
    <!-- this will expand between header/footer -->
    <router-view />
  </main>
  <Foot />
 </template>
