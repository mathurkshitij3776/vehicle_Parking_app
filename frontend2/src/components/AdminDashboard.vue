
<template>
  <div>
    <div v-if="!token">LOG in First</div>
    <div v-else>
      <!-- <h2>WELCOME To Admin DASHBOARD</h2> -->
      <div v-if="error">{{ error }}</div>
      <div v-if="Parkinglots.length === 0">NO parking lots</div>
      <div class="container my-4" v-else>
        <div class="row">
          <div class="col-md-6 mb-4"
               v-for="(lot, idx) in Parkinglots" :key="lot.id">
            <div class="card">
              <div class="card-body">
                <h5 class="text-center">Parking Lot #{{ idx + 1 }}</h5>
                <p class="text-center mb-2">
                  <button @click="deletelot(lot.id)" class="btn btn-primary">Delete</button> |
                  <button @click="this.$router.push(`/editparkinglot/${lot.id}`)" class="btn btn-primary">Edit</button>
                </p>
                <h6 class="text-center text-muted mb-2">
                  (Occupied - {{ lot.Occupied }}/{{ lot.maxspots }})
                </h6>
                <div class="d-flex flex-wrap justify-content-center">
                  <button @click="$router.push(`/spot/${spot.id}`)" v-for="spot in lot.spots" :key="spot.id" type="button" class="btn btn-outline-info m-1" style="width: 50px;">
                    {{ spot.status }}
                  </button>
                </div>
              </div>
            </div>
          </div>
         
        </div>
        
      </div>
      <p v-if="error" class="text-danger">{{ error }}</p>
    </div>
     <button @click="$router.push('/Addparkinglot')" class="btn btn-success">
          Add parking lot
        </button>
  </div>
  
</template>



<script>

import axios from 'axios';

export default {
  data() {
    return {
      Parkinglots: [],
      token: "",
      error: "",
      role:""
    };
  },
  mounted(){
    this.token = localStorage.getItem('token');
    // if (this.token) {this.loadLots();}
    
    this.loadLots();
  },
  methods: {
    deletelot(id){
      axios.delete(`http://127.0.0.1:5000/api/deleteParkinglot/${id}`, {
         headers:{
          "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                'Authorization': `Bearer ${this.token}`  
        }
    }).then(res=>{
        // this.$router.push('/AdminDashboard')
      // alert(res.data.message);
      this.loadLots();
    }).catch(err=>{
      
      alert('NOt Deleted ');
    })
    },
    loadLots() {
      axios.get('http://127.0.0.1:5000/api/AdminDashboard', {
        headers: {
           'Content-Type': 'application/json',
           "Access-Control-Allow-Origin": "*", 
          'Authorization': `Bearer ${this.token}`
        }
      })
      .then(res => {
        this.Parkinglots = res.data.parkinglots;
      })
      .catch(err => {
        console.error(err);
        this.error = err.response.data.message;
      });
    }
  }
}
</script>

<!-- //         import axios from 'axios';
//         export default {
//             data(){
//                 return {
//                     Parkinglots: "",
//                     token: "",
//                     error: ""
//                 }
//             },
//             mounted(){
//                 this.loadtoken()
//                 this.loaduser()
//             },
//             methods:{
//                 //logoutuser(){},
//                 loadtoken(){
//                     {this.token = localStorage.getItem('token')}
//                 },
//                 loaduser(){
//                     axios.get('http://127.0.0.1:5000/AdminDashboard', {
//                         headers: {
//                             "Content-Type": "application/json",
//                             "Access-Control-Allow-Origin": "*",
//                             "Authorization": `bearer ${this.token}`
//                         }
//                     }
//                 ).then(res={
//                        this.Parkinglots = res.data.parkinglots;

//                 })
//             }
//             }
//         }




//  -->


