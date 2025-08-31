<!-- <template>

<form @submit.prevent="booking">
<div class="card text-bg-primary mb-3" style="max-width: 18rem;">
  <div class="card-header">Book the parking spot</div>
  <div class="card-body">
    <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">LOTID</label>
            <input type="text" class="form-control" v-model="space.lotid" id="exampleInputEmail1" disabled>
          </div>
          <div class="mb-3">
            <label for="exampleInputEmail2" class="form-label">SPOTID</label>
            <input type="text" class="form-control" v-model="space.spotid" id="exampleInputEmail2" disabled>
          </div>
          <div class="mb-3">
            <label for="exampleInputEmail3" class="form-label">USERID</label>
            <input type="text" class="form-control" v-model="space.userid" id="exampleInputEmail3" disabled>
          </div>
          <div class="mb-3">
            <label for="exampleInputEmail5" class="form-label">Rate</label>
            <input type="text" class="form-control" v-model="space.rate" id="exampleInputEmail5" disabled>
          </div>
          <div class="mb-3">
            <label for="exampleInputEmail4" class="form-label">Vehicle number</label>
            <input type="text" class="form-control" v-model="space.vehiclenumber" id="exampleInputEmail4" required>
          </div>
  </div>
<input type="submit" class="btn btn-success" id="exampleInputEmail6" />

</div>
</form>
</template>

<script>
import axios from 'axios';

export default {
    data(){
        return{
            space:{
                lotid:"",
                spotid:"",
                userid:"",
                vehiclenumber:"",
                rate:null
                
            },
            spots:[]
        }
    },

    mounted(){
        this.token = localStorage.getItem('token');
        
        this.loadlot();
        
    },
    methods:{
        booking(){
                axios.post('http://127.0.0.1:5000/book/reservation', JSON.stringify(this.space),{
                    headers:{
                         "Content-Type": "application/json",
                         "Access-Control-Allow-Origin": "*",
                         'Authorization': `Bearer ${this.token}`
                          }
                  }).then(res=>{
                        this.$router.push('/UserDashboard');
                  }).catch(err=>{
                    alert('not booked');
                
                  })

        },
        loadlot(){
            const lid = this.$route.params.id
            this.userid = localStorage.getItem('userid');
            console.log(userid)
            axios.get(`http://127.0.0.1:5000/api/lotdetails/${lid}`, {
                
                     headers:{
                         "Content-Type": "application/json",
                         "Access-Control-Allow-Origin": "*",
                         'Authorization': `Bearer ${this.token}`
        }
                }).then(res=>{
                    let d = res.data.result
                    this.space.lotid = this.$route.params.id
                    this.space.spotid = d.spotid
                    this.space.rate = d.rate
                    this.space.userid = d.userid
                    
                }).catch(err=>{
                          alert('no booked')
                })
        }
    }
}



</script>


<style scoped>


.login_form{
    border: 2px solid  green;
    padding: 20px;
    height: 400px;
    width: 400px;
    margin: auto;
    padding-bottom: 0px;
    border-radius: 10%;
    

}



</style> -->
<template>
  <div v-if="loaded">
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <form v-else @submit.prevent="booking">
      <div class="card text-bg-primary mb-3" style="max-width: 18rem;">
        <div class="card-header">Book the parking spot</div>
        <div class="card-body">
          <div class="mb-3">
            <label class="form-label">LOT ID</label>
            <input class="form-control" v-model="space.lotid" disabled />
          </div>
          <div class="mb-3">
            <label class="form-label">SPOT ID</label>
            <input class="form-control" v-model="space.spotid" disabled />
          </div>
          <div class="mb-3">
            <label class="form-label">USER ID</label>
            <input class="form-control" v-model="space.userid" disabled />
          </div>
          <div class="mb-3">
            <label class="form-label">Rate (₹/hr)</label>
            <input class="form-control" v-model="space.rate" disabled />
          </div>
          <div class="mb-3">
            <label class="form-label">Vehicle number</label>
            <input class="form-control" v-model="space.vehiclenumber" required />
          </div>
          <button type="submit" class="btn btn-success">Reserve</button>
        </div>
      </div>
    </form>
  </div>
  <div v-else>
    <p>Loading lot details…</p>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      loaded: false,
      error: "",
      token: localStorage.getItem('token') || "",
      space: {
        lotid: "",
        spotid: "",
        userid: "",
        vehiclenumber: "",
        rate: null
      }
    };
  },
  mounted() {
    if (!this.token) {
      this.error = "You must be logged in.";
      this.loaded = true;
      return;
    }
    this.loadlot();
  },
  methods: {
    loadlot() {
      const lotId = this.$route.params.id;
    //   console.log(this.token)
      axios.get(`http://127.0.0.1:5000/api/lotdetails/${lotId}`, {
        headers: { Authorization: `Bearer ${this.token}` }
      })
      .then(res => {
        this.space.lotid = res.data.result.lotid
        this.space.spotid = res.data.result.spotid
        this.space.rate = res.data.result.rate
        this.space.userid = res.data.result.userid
    })
      .catch(err => {
        // console.error("loadlot() error:", err);
        // this.error = err.response?.data?.error || err.message || "Failed to load lot.";
      this.error = err.data.result.message
    })
      .finally(() => {
        this.loaded = true;
      });
    },
    
    booking() {
      axios.post('http://127.0.0.1:5000/book/reservation', this.space, {
        headers: { Authorization: `Bearer ${this.token}` }
      })
      .then(() => {
        this.$router.push('/UserDashboard');
      })
      .catch(err => {
        console.error("booking() error:", err);
        this.error = err.response?.data?.error || "Booking failed.";
      });
    }
  }
};
</script>
