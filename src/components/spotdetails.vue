<template>
<div class="container">
    <div class="box">
      <div class="login_form">
        <h2 style="padding-bottom: 0px; text-align:center">VIew/delete parking spot</h2>

        
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">ID</label>
            <input type="number" class="form-control" v-model="spot.id" id="exampleInputEmail1" disabled>
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Status</label>
            <input type="text" v-if="spot.status==='A'" class="form-control" v-model="spot.status" id="exampleInputPassword1" disabled>
            <input @click="$router.push(`/occupied/${spot.id}`)" type="button" v-else  class="form-control " v-model="spot.status" id="exampleInputPassword1" ></input>
          
          </div>
           <div class="mb-3">
            <label for="exampleInputPassword2" class="form-label">primelocation</label>
            <input type="text" class="form-control" v-model="spot.primelocation" id="exampleInputPassword2" disabled>
          </div>
        

          <div style="text-align: center; padding:15px">
            <!-- <input type="submit" class="btn btn-success" value="Login"> -->
            <button @click="deletespot(spot.id)" class="btn btn-primary">Delete</button>
            <router-link to="/AdminDashboard" class="btn btn-primary">Cancel</router-link>

          </div>

          <!-- Show error message -->
       
      </div>
    </div>
  </div>


</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            spot:{},
            token:""
        }
    },
    mounted(){
        this.token = localStorage.getItem('token');
        this.loadspotdetails();
    },
    methods:{
           deletespot(id){
            axios.delete(`http://127.0.0.1:5000/api/deleteParkingspot/${id}`,  {
         headers:{
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          'Authorization': `Bearer ${this.token}`
        }
    }).then(res=>{
        this.$router.push('/AdminDashboard');
        
    }).catch(err=>{
        alert('spot is not deleted')
    })
           },
           loadspotdetails(){
            console.log('before id');
            const sid = this.$route.params.id
            console.log('after id', sid);
               axios.get(`http://127.0.0.1:5000/api/viewparkingspot/${sid}`, {
                headers:{
                    "Content-Type": "application/json",
                     "Access-Control-Allow-Origin": "*",
                     'Authorization': `Bearer ${this.token}`
                }
               }).then(res=>{
                this.spot = res.data
                

               }).catch(err=>{
                  alert('spot not found');
               })
           }
    }
}
</script>