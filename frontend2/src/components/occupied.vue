<template>
<div class="container">
    <div class="box">
      <div class="login_form">
        <h2 style="padding-bottom: 0px; text-align:center">Spot details</h2>

        
          <div class="mb-3">
            <label  class="form-label">ID</label>
            <input type="text" class="form-control" v-model="spot.spotid" disabled>
          </div>
          <div class="mb-3">
            <label  class="form-label">CUSTOMER ID</label>
            <input type="text" class="form-control" v-model="spot.userid"  disabled>
          </div>
          <div class="mb-3">
            <label  class="form-label"> VIHECLE NUMBER </label>
            <input type="text" class="form-control"  v-model="spot.viheclenumber"  disabled>
          </div><div class="mb-3">
            <label  class="form-label">PARKING TIME </label>
            <input type="text" class="form-control" v-model="spot.date"  disabled>
          </div><div class="mb-3">
            <label  class="form-label"> COST </label>
            <input type="text" class="form-control" v-model="spot.cost" disabled>
          </div>
          <div style="text-align: center; padding:15px">
            <!-- <input type="submit" class="btn btn-success" value="Login"> -->
            
            <router-link :to="(`/spot/${$route.params.id}`)" class="btn btn-primary">Cancel</router-link>

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
        this.spotdet();
    },
    methods:{
           spotdet()
              {
                const id =this.$route.params.id
                // if (!id) {
                // alert("Route param ID not available");}
                 axios.get(`http://127.0.0.1:5000/api/spotdetails/${id}`,  {
                   headers:{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    'Authorization': `Bearer ${this.token}`
                  }
    }).then(res=>{
        this.spot = res.data.spot

        
    }).catch(err=>{
        alert('no working')
    })
           }
           
    }
}
</script>