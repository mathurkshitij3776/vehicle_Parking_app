<template>
    <h1>{{ error }}</h1>
  
    <div class="container">
    <div class="box">
      <div class="login_form">
        <h2 style="padding-bottom: 0px; text-align:center">New Parking Lot</h2>

        <form @submit.prevent="editparkinglot">
          <div class="mb-3">
            <label for="primelocation" class="form-label">Prime location Name</label>
            <input type="text" class="form-control" v-model="formdata.primelocation" id="primelocation"  required>
          </div>
          <div class="mb-3">
            <label for="Address" class="form-label">Address</label>
            <textarea type="text" class="form-control" v-model="formdata.address" id="Address" required></textarea>
          </div>
          <div class="mb-3">
            <label for="Pincode" class="form-label">Pin code</label>
            <input type="text" class="form-control" v-model="formdata.pincode" id="Pincode"  required>
          </div>
          <div class="mb-3">
            <label for="Priceperhour" class="form-label">Price per hours</label>
            <input type="number" class="form-control" v-model="formdata.priceperhour" id="Priceperhour"  required>
          </div>
          <div class="mb-3">
            <label for="Maximumspots" class="form-label">Maximam Spots</label>
            <input type="number" class="form-control" v-model="formdata.maxspots" id="Maximumspots"  required>
          </div>

          <div style="text-align: center; padding:15px">
            <input type="submit" class="btn btn-success" value="submit">
            <router-link to="/AdminDashboard" class="btn btn-primary">Cancel</router-link>
          </div>

          <!-- Show error message -->
          <!-- <p v-if="error" style="text-align: center; color: red;">{{ error }}</p> -->
        </form>
      </div>
    </div>
  </div>


</template>
<script> 
import axios from 'axios';

    export default{
        data(){
            return {
                formdata:{
                primelocation: "",
                address: "",
                pincode: "",
                priceperhour: "",
                maxspots: ""
            },
            token: ""
        }
    },
    mounted(){
         this.loadtoken();
         this.geteditparkinglot();
    },
    methods:{
      loadtoken(){
                    this.token = localStorage.getItem('token')
                    console.log("Token mila:", this.token);
                },
       geteditparkinglot() {
      // this.error = "";
      const id = this.$route.params.id
      axios.get(`http://127.0.0.1:5000/api/editParkinglot/${id}`, {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization": `Bearer  ${this.token}`
        }
      })
      .then(res => {
             this.formdata = res.data.formdata  
          }).catch(err => {
      console.error("Error:", err);
      alert("Failed to edit parking lot");
    });
    },
    editparkinglot() {
      // this.error = "";
      const id = this.$route.params.id
      axios.put(`http://127.0.0.1:5000/api/editParkinglot/${id}`, JSON.stringify(this.formdata), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization": `Bearer  ${this.token}`
        }
      })
      .then(res => {
             this.$router.push('/AdminDashboard')  
          }).catch(err => {
      console.error("Error:", err);
      alert("Failed to edit parking lot");
    });
    }
}
    }
</script>