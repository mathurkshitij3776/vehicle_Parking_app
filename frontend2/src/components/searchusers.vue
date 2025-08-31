<script>
import axios from 'axios';

export default{
    data(){
        return{
            users:[],
            token:""
        }
    },
    mounted(){
        this.token = localStorage.getItem('token');
        this.fetcusers();
    },
    methods:{
        fetcusers(){
            axios.get('http://127.0.0.1:5000/api/allusers', {
                headers:{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    'Authorization': `Bearer ${this.token}`
                }
            }).then(res=>{
                this.users = res.data.users
            }).catch(err=>{
                alert('NO users')
            })
        }
    }
}
</script>

<template><div>
  <h2 v-if="users.length === 0"> No space available at this location</h2>
  
  <table class="table table-dark table-striped" >
    
  <thead>
    <tr>
      <th scope="col">id</th>
      <th scope="col">username</th>
      <th scope="col">Full name</th>
      <th scope="col">address</th>
      <th scope="col">Pincode</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(user, idx) in users" :key="user.id">
      <th scope="row">{{ user.id }} </th>
      <td>  {{ user.username }} </td>
      <td>  {{ user.fullname }} </td>
      <td>  {{ user.location }} </td>
      <td>  {{ user.pincode }} </td>
    </tr>
    
  </tbody>
</table>
            </div>
            </template>












