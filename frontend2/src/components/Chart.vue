<!-- <template>
  <div class="summary-charts">
    <h2 style="margin-bottom: 20px;">📊 Summary Dashboard</h2>

    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 2rem">
      <div style="width: 400px">
        <h3>💰 Revenue from Lots</h3>
        <Pie :data="revenueData" :options="chartOptions" />
      </div>

      <div style="width: 400px">
        <h3>🚗 Parking Spot Status</h3>
        <Bar :data="statusData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script>
import { Pie, Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import axios from 'axios';

ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale);

export default {
  name: 'SummaryCharts',
  components: { Pie, Bar },
  data() {
    return {
        token:"",
      revenueData: null,
      statusData: null,
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom'
          },
          title: {
            display: false
          }
        }
      }
    };
  },
  mounted() {
    this.token = localStorage.getItem('token')
    this.getRevenue();
    this.getStatus();
  },
  methods: {
    getRevenue() {
      axios.get('http://127.0.0.1:5000/revenue', {
        headers:{
            "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    'Authorization': `Bearer ${this.token}`
        }
      })
        .then(res => {
          const data = res.data.revenue;
          const labels = Object.keys(data).map(lotId => `Lot ${lotId}`);
          const values = Object.values(data);
          this.revenueData = {
            labels: labels,
            datasets: [
              {
                label: 'Revenue (₹)',
                data: values,
                backgroundColor: this.generateColors(values.length)
              }
            ]
          };
        })
        .catch(err => console.log(err));
    },

    getStatus() {
      axios.get('/spot-status')
        .then(res => {
          const data = res.data.summary;
          const labels = Object.keys(data);
          const values = Object.values(data);
          this.statusData = {
            labels: labels,
            datasets: [
              {
                label: 'Spots',
                data: values,
                backgroundColor: ['#36A2EB', '#FF6384']
              }
            ]
          };
        })
        .catch(err => console.log(err));
    },

    generateColors(count) {
      const base = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
      return Array.from({ length: count }, (_, i) => base[i % base.length]);
    }
  }
};
</script>

<style scoped>
.summary-charts {
  padding: 2rem;
  font-family: sans-serif;
  color: #333;
}

h2, h3 {
  text-align: center;
}
</style> -->
<template>
  <div v-if="role!='user'" class="dashboard-container">
    <h2> revenue by Parking Lot </h2>
    <canvas id="revenueChart" width="50" height="50"></canvas>

    <h2 class="mt-4">Parking Lot Spot Status</h2>
    <canvas id="statusChart" width="300" height="300"></canvas>
  </div>
  <div v-else class="dashboard-container2">
    <h2 class="mt-42"> Parking History </h2>
    <canvas id="parkinghistory" width="250" height="250"></canvas>

  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'AdminDashboard',
  data(){
    return{
        token: "",
        role:""
    }
  },
  mounted(){
    this.token = localStorage.getItem('token');
    this.role = localStorage.getItem('role');
    if (this.role !='user'){
         this.revenue();
    
         this.fstatus();}
    else
        {this.reservationhistory();
                                }
  },

  methods:{
    revenue(){
     axios.get('http://127.0.0.1:5000/revenue', {
      headers: {  "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                'Authorization': `Bearer ${this.token}`
             }
    }).then(res => {
      const data = res.data.revenue
      const lotIds = Object.keys(data)
      const values = Object.values(data)

      new Chart(document.getElementById('revenueChart'), {
        type: 'pie',
        data: {
          labels: lotIds.map(id => 'Lot ' + id),
          datasets: [{
            label: 'Revenue',
            data: values,
            backgroundColor: ['#1abc9c', '#3498db', '#9b59b6', '#e74c3c']
          }]
        }
      })
    }).catch(err => console.log(err))},
    
    fstatus(){
        axios.get('http://127.0.0.1:5000/status', {
      headers: {  "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                'Authorization': `Bearer ${this.token}` }
    }).then(res => {
      const status = res.data.status
      const lotIds = Object.keys(status)
      const occupied = []
      const available = []

      lotIds.forEach(id => {
        occupied.push(status[id].occupied)
        available.push(status[id].available)
      })

      new Chart(document.getElementById('statusChart'), {
        type: 'bar',
        data: {
          labels: lotIds.map(id => 'Lot ' + id),
          datasets: [
            {
              label: 'Occupied',
              data: occupied,
              backgroundColor: '#e74c3c'
            },
            {
              label: 'Available',
              data: available,
              backgroundColor: '#2ecc71'
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }).catch(err => console.log(err))
   
  },
   reservationhistory(){
     let userid = localStorage.getItem('userid')
     axios.get(`http://127.0.0.1:5000/history/reservations/${userid}`, {
      headers: {  "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                'Authorization': `Bearer ${this.token}`
             }
    }).then(res => {
      const reserved = res.data.reserved
      const locations = Object.keys(reserved)
      const values = Object.values(reserved)

      // locations.forEach(id => {
      //   occupied.push(status[id].occupied)
      //   available.push(status[id].available)
      // })

      new Chart(document.getElementById('parkinghistory'), {
        type: 'bar',
        data: {
          labels: locations,
          datasets: [
            {
              label: 'frequency',
              data: values,
              backgroundColor: '#e74c3c'
            // },
            // {
            //   label: 'Available',
            //   data: available,
            //   backgroundColor: '#2ecc71'
            // 
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }).catch(err => console.log(err))
   }
}}
    
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 400px;
  margin: auto;
}
.mt-4 {
  margin-top: 40px;
}

.dashboard-container2 {
  padding: 20px;
  max-width: 400px;
  margin: auto;
}
.mt-42 {
  margin-top: 40px;
}
</style>
