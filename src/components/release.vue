<template>
  <h1 v-if="error">{{ error }}</h1>
    
      <div v-else class="card text-bg-primary mb-3" style="max-width: 18rem;">
        <div class="card-header">Book the parking spot</div>
        <div class="card-body">
          <!-- spotdetails ={
        "spotid" : reserve.spot_id,
        "viheclenumber": reserve.vichel_number,
        "parkingstamp" : reserve.parking_timestamp,
        "leavingstamp" : now,
        "rate": rate,
        "cost": cost
    } -->
                <div class="mb-3">
                  <label class="form-label">SPOT ID</label>
                  <input class="form-control" v-model="spotdetails.spotid" disabled />
                </div>
                <div class="mb-3">
                  <label class="form-label">vehiclenumber</label>
                      <input class="form-control" v-model="spotdetails.viheclenumber" disabled />
                </div>
                  <div class="mb-3">
                     <label class="form-label">parkingtimestamp</label>
                  <input class="form-control" v-model="spotdetails.parkingstamp" disabled />
                </div>
                <div class="mb-3">
                    <label class="form-label">leavingtimestamp</label>
                  <input class="form-control" v-model="spotdetails.leavingstamp" disabled />
                  </div>
                  <div class="mb-3">
                  <label class="form-label">Totalcost</label>
                  <input class="form-control" v-model="spotdetails.cost" disabled/>
                  </div>
                    <button @click="release(spotdetails.id, spotdetails.cost)" type="submit" class="btn btn-success">Release </button> 
                <router-link to="/UserDashboard" class="btn btn-success">cancel</router-link>
        
        </div>
      </div>
   
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            spotdetails:{},
            token:"",
            error:"",
            timer:"",
            message:""
        }
       
    },
    mounted(){
      this.token = localStorage.getItem('token')
      this.spotd();
      this.timer = setInterval(this.spotd, 60000);

    },
     unmounted(){ clearInterval(this.timer);},
     methods:{
       spotd(){
              const rid = this.$route.params.id
              axios.get(`http://127.0.0.1:5000/release/${rid}`, {
                headers:{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    'Authorization': `Bearer ${this.token}`
                }
              }).then(res=>{
                this.spotdetails = res.data.spotdetails
                
              }).catch(err=>{
                this.error = err.data.err
              })
            },
            release(id,cost){
              axios.post(`http://127.0.0.1:5000/release/${id}`, 
                {cost: cost},
                {headers:{
                  "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    'Authorization': `Bearer ${this.token}`
                }}
               ).then(res=>{
                   this.$router.push('/UserDashboard')
               }).catch(err=>{
                alert('Not released')
               })
            }


          }}

</script>