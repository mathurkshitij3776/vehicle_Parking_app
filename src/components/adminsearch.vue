<template>
<div>
<select v-model="searchterm" class="form-select" aria-label="Default select example">
  <option selected >Search by</option>
  <option value="location">location</option>
  <option value="userid">User id</option>
  <option value="username">username</option>
  <option value="pincode">pincode</option>
</select>
<button type="button" class="btn btn-outline-primary" disabled>{{ term }}</button>

<input type="text" class="form-control" v-model="term">
<button @click="adminsearch" type="button" class="btn btn-outline-primary">search</button>
</div>
<div class="container my-4" v-if="searchterm==='location' || searchterm ==='pincode'">
        <div class="row">
          <div class="col-md-6 mb-4"
               v-for="(lot, idx) in info" :key="lot.id">
            <div class="card">
              <div class="card-body">
                <h5 class="text-center">Parking Lot #{{ idx + 1 }}</h5>
                <p class="text-center mb-2">
                  <button @click="deletelot(lot.id)" class="btn btn-primary">Delete</button> |
                  <button  class="btn btn-primary">Edit</button>
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
            </div></div>
        </div>
</div>

<div class="container my-4" v-if="searchterm==='userid' || searchterm==='username'">
    <div class="row" style="padding-left: 400px;" >
         <div class="card text-bg-info mb-3" style="max-width: 18rem;">
  <div class="card-header"></div>
  <div class="card-body">
    
                   <p class="card-text"> user id - {{ info.id }}</p>
                   <p class="card-text">user name - {{ info.fullname }}</p>
                   <p class="card-text">user username{{ info.username}}</p>
                   <p class="card-text">user location{{ info.location }}</p>
                   <p class="card-text">user  pincode{{ info.pincode }}</p>
                   <p class="card-text">user role {{ info.category }}</p>
  </div>
</div>
    </div></div>

</template>
<script>
import axios from 'axios';

export default{
    data(){
        return{
            info:"",
            token:"",
            term:"",
            searchterm:"" 
        }
    },
    mounted(){
        this.token = localStorage.getItem('token')
    },
    methods:{
        adminsearch(){
            axios.get('http://127.0.0.1:5000/api/search/admin', 
               { params:{term: this.term, category: this.searchterm},
            headers:{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                'Authorization': `Bearer ${this.token}`
            }
            }
            ).then(res=>{
                this.info= res.data.info
            }).catch(err=>{
                
                alert('Something wrong')
            })
        }
    }
}
</script>