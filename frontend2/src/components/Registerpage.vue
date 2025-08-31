<script>
import axios from 'axios';
export default{
  data(){
    return {
      formdata:{
        username: "",
        password:"",
        fullname:""
      },
      msg:"",
      error:""
    }
  },
  methods:{
    registeruser(){
    this.error = "";
    this.msg = "";
      axios.post('http://127.0.0.1:5000/api/register', JSON.stringify(this.formdata), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      })
      .then(res => {
        // this.token = res.data.access_token;
        // localStorage.setItem("token", res.data.access_token);
        // this.role = res.data.role;
          this.msg = res.data.message;

          })
      .catch(err => {
        this.error = err.response.data.message;    //|| "Login failed"
      })
    }
  }
}
</script>


<template> <div class="container">
        <div class="box">
          <div class="register_form">
            <h2 style="padding-bottom: 0px; text-align:center">Register</h2>
            <form @submit.prevent="registeruser" method="post" >
              <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label" >Username</label>
                <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model = "formdata.username" required>
                
              </div>
              <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label"> Password</label>
                <input type="password" class="form-control" id="exampleInputPassword1" v-model = "formdata.password">
              </div>
              <div class="mb-3">
                <label for="exampleInputfullname" class="form-label"> Fullname</label>
                <input type="text" class="form-control" id="exampleInputfullname" v-model = "formdata.fullname">
              </div>
              <!-- <div class="mb-3">
                <label for="exampleInputDOB" class="form-label"> Date of birth</label>
                <input type="date" class="form-control" id="exampleInputDOB" name = "DOB">
              </div> -->
              <div style=  "text-align: center">
                <input type="submit" class="btn btn-success" value="Register" style="text-align: center;">
              <button @click="this.$router.push('/login')" class="btn btn-primary">Go to login</button>
              <h3 v-if="msg" style="text-align: center;" >{{msg}}</h3>   
              <h3 v-if="error" style="text-align: center;" >{{error}}</h3>   
            
            </div>

            </form>
            
            
          </div>
        </div>
      </div>
      </template>



<style scoped>
.register_form{
    border: 2px solid green;
    padding: 20px;
    height: 430px;
    width: 400px;
    margin: auto;
    padding-bottom: 0px;
    margin-top: 76px;
    font-size: 13px;
    border-radius: 10%;
}</style>