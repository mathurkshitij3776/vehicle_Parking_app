<template>
    <h2 v-if="reservations.length===0"> No parking History </h2>


<table v-if = "token && reservations.length" class="table table-dark table-striped">
  <thead>
    <tr>
      <th scope="col">id </th>
      <th scope="col"> Location  </th>
      <th scope="col">vehicle Number  </th>
      <th scope="col">Timestamp  </th>
      <th scope="col"> Action </th>

    </tr>
  </thead>
  <tbody>
    <tr v-for="(reserve, ind) in reservations " :key="reserve.id">
      <th scope="row"> {{ reserve.id }}</th>
      <td>{{ reserve.location }}</td>
      <td>{{ reserve.vichelnumber }}</td>
      <td>{{ reserve.parkingtimestamp }}</td>
      <button @click="this.$router.push(`/release/${reserve.id}`)" v-if="reserve.leavingtimestamp===null">Release</button>
      <td v-else> <button disabled>parked out</button></td>
    </tr>
    
  </tbody>
</table>
<br>       
<form @submit.prevent="searchspots">

        <div class="mb-3">

         <label for="exampleInputEmail6" class="form-label">Search Parking @location/pin code {{ terms}}</label>
         <br>
            <input type="text" class="form-control" v-model="terms" id="exampleInputEmail6">
            <input type="submit" class="btn btn-primary"id="exampleInputEmail6" />
        </div>
        </form>

<div>
  <h2 v-if="spots.length === 0 && load"> No space available at this location</h2>
  <table class="table table-dark table-striped" >
    
  <thead>
    <tr>
      <th scope="col">id</th>
      <th scope="col">address</th>
      <th scope="col"> available </th>
      <th scope="col">Action</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(l, idx) in spots" :key="l.id">
      <th scope="row">{{ idx + 1 }} </th>
      <td>  {{ l.address }} </td>
      <td>  {{ l.availability }} </td>
     <td><button @click="this.$router.push(`/lotdetails/${l.id}`)">  Book </button> </td>
    </tr>
    
  </tbody>
</table>
            </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            token: "",
            reservations: [],
            terms:"",
            spots:[],
            load: false
        }
    },
    
    mounted(){
        this.token = localStorage.getItem('token');
        console.log('Token:', this.token); 
        this.parkinghistory();
        
    },
    methods:{
        searchspots(){
          if (!this.token){
            alert('LOGIN FIRST');
          }
            axios.get('http://127.0.0.1:5000/api/alllotdetails', {
                params:{term: this.terms},
                headers:{
                         "Content-Type": "application/json",
                         "Access-Control-Allow-Origin": "*",
                         'Authorization': `Bearer ${this.token}`
                          }
            }).then(res=>{
                    this.spots = res.data.result
                    this.load = true
            }).catch(err=>{
              alert('')
            })
        },
        parkinghistory(){
            const uid=  localStorage.getItem('userid')
            axios.get(`http://127.0.0.1:5000/history/reservation/${uid}`, {
                
                     headers:{
                         "Content-Type": "application/json",
                         "Access-Control-Allow-Origin": "*",
                         'Authorization': `Bearer ${this.token}`
        }
                }
            ).then(res=>{
                this.reservations = res.data.reservations;
            })
        }  ,
        loadlots(){

          axios.get(`http://127.0.0.1:5000/get/reservations/${this.lot}`,{
          headers:{
                                "Content-Type": "application/json",
                                "Access-Control-Allow-Origin": "*",
                                'Authorization': `Bearer ${this.token}`
               }
          }).then(res=>{
                this.lots = res.data.lots;

          })
        }
    }
}


</script>