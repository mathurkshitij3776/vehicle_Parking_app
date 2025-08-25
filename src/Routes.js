import {createWebHistory, createRouter} from 'vue-router';
import Loginpage from "./components/Loginpage.vue";
import Registerpage from './components/Registerpage.vue';
import Home from './components/Home.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import Addparkinglot from './components/Addparkinglot.vue';
import spotdetails from './components/spotdetails.vue';
import { computed } from 'vue';
import UserDashboard from './components/UserDashboard.vue';
import lotdetails from './components/lotdetails.vue';
import release from './components/release.vue';
import occupied from './components/occupied.vue';
import Users from './components/searchusers.vue';
import Adminsearch from './components/adminsearch.vue';
import Editparkinglot from './components/editparkinglot.vue';
import Chart from './components/Chart.vue';
const routes = [
    {path:'/', component : Home },
    {path:'/login', component : Loginpage },
    {path:'/AdminDashboard', component: AdminDashboard},
    {path:'/register', component : Registerpage },
    {path:'/Addparkinglot', component: Addparkinglot},
    {path:'/spot/:id', name:'spotdetials' ,component: spotdetails},
    {path:'/UserDashboard', component: UserDashboard},
    {path:'/lotdetails/:id', component: lotdetails},
    {path:'/release/:id', component:release},
    {path:'/occupied/:id', component: occupied},
    {path:'/searchusers', component: Users},
    {path:'/adminsearch', component: Adminsearch},
    {path:'/editparkinglot/:id', component: Editparkinglot},
    {path:'/Chart', component: Chart}

]


export const router = createRouter({
    history: createWebHistory(),
    routes
})

