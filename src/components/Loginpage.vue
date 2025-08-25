<!-- <script>
import axios from 'axios';
    export default{
        data(){
            return {
                formdata: {
                    username : "",
                    password : ""
                },
                token : "",
                error : ""
            }
        },
        methods : {
            loginuser(){
                const response = axios.post('http://127.0.0.1:5000/login' , JSON.stringify(this.formdata),{
                     headers:{
                     "Content-Type": "application/json",
                     "Allow-Access-Allow-Control": "*"
                }}
            )
            response
            .then(res=>{
                
                    this.token = res.data.access_token
                    localStorage.setItem("token", res.data.access_token)
                    this.$router.push('/Dashboard')
          
            }

            ).catch(err => this.error = err.response.data.mesaage)
            }
        }
    }


</script>
<template>
    <h1 class="display-4 text-center text-decoration-underline ">WELCOME TO VICHEL PARKING APP</h1>
      <div class="container">
        <div class="box">
         
          <div class="login_form">
            <h2 style="padding-bottom: 0px; text-align:center">Login</h2>
            
            <form @submit.prevent = "loginuser">
              <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">Username</label>
                <input type="email" class="form-control" v-model="formdata.username" id="exampleInputEmail1" aria-describedby="emailHelp" required>
                <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
              </div>
              <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label"> Password</label>
                <input type="password" class="form-control" v-model="formdata.password" id="exampleInputPassword1" required>
              </div>
              
              <div style="text-align: center; padding:15px">
              <input type="submit" class="btn btn-success" value="Login" style="text-align: center;">
              <button @click="this.$router.push('/register')" class="btn btn-primary">New user registration</button></div>
                <p style="text-align: center;">{{msg}}</p>   
            </form>


            
          </div>
        </div>
      </div>

</template>
<style>
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
<script>
import axios from 'axios';

export default {
  data() {
    return {
      formdata: {
        username: "",
        password: ""
      },
      token: "",
      error: "",
      role: ""
    }
  },
  methods: {
    loginuser() {
      this.error = "";
      axios.post('http://127.0.0.1:5000/api/login', JSON.stringify(this.formdata), {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      })
      .then(res => {
        this.token = res.data.access_token;
        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("role", res.data.role);
        localStorage.setItem('userid', res.data.auser.id);
        this.role = res.data.role;
        if (this.role === 'admin'){ 
           this.$router.push('/AdminDashboard');
        }
        else{ this.$router.push('/UserDashboard')

        }
          })
      .catch(err => {
        this.error = err.response?.data?.message;    //|| "Login failed"
      });
    }
  }
}
// import axios from 'axios';

// export default {
//   data() {
//     return {
//       formdata: {
//         username: "",
//         password: ""
//       },
//       token: "",
//       error: "",
//       role: ""
//     }
//   },
//   methods: {
// loginuser() {
//   this.error = "";
//   axios.post('http://127.0.0.1:5000/login', JSON.stringify(this.formdata), {
//     headers: {
//       "Content-Type": "application/json"
//     }
//   })
//   .then(res => {
//     this.token = res.data.access_token;
//     localStorage.setItem("token", res.data.access_token);
//     this.role = res.data.role;

//     if (this.role === 'admin') {
//       this.$router.push('/AdminDashboard');
//     } else {
//       this.$router.push('/UserDashboard');
//     }
//   })
//   .catch(err => {
//     console.log("Login Error: ", err.response?.data);  // Debug log
//     this.error = err.response?.data?.message || "Login failed";
//   });
// }}}

</script>


<template>
  <h1 class="display-4 text-center text-decoration-underline">WELCOME TO VEHICLE PARKING APP</h1>
  <div class="container">
    <div class="box">
      <div class="login_form">
        <h2 style="padding-bottom: 0px; text-align:center">Login</h2>

        <form @submit.prevent="loginuser">
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">Username</label>
            <input type="email" class="form-control" v-model="formdata.username" id="exampleInputEmail1" aria-describedby="emailHelp" required>
            <div id="emailHelp" class="form-text"></div>
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">Password</label>
            <input type="password" class="form-control" v-model="formdata.password" id="exampleInputPassword1" required>
          </div>

          <div style="text-align: center; padding:15px">
            <input type="submit" class="btn btn-success" value="Login">
            <button @click="this.$router.push('/register')" class="btn btn-primary">New user registration</button>
          </div>

          <!-- Show error message -->
          <p v-if="error" style="text-align: center; color: red;">{{ error }}</p>
        </form>
      </div>
    </div>
  </div>
</template>


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
</style>