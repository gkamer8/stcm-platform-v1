<template>
  <div id="app">
    <NavBar></NavBar>
    <br/>
    <main style="padding-top: 30px;" class="site__content mt-5">
        <router-view></router-view>
    </main>
  </div>
</template>


<!-- <script src="https://unpkg.com/ionicons@5.1.2/dist/ionicons.js"></script> -->
<script>
// import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import NavBar from './components/NavBar.vue'
import '@mdi/font/css/materialdesignicons.css'
// import VueRouter from 'vue-router'

Vue.use(Buefy);

export default {
  name: 'App',
  components: {
    NavBar
  },
  data: function(){
    return {
        greeting: 'Hello, Vue!',
        flaskGreeting: ''
    }
  },
  created() {
    this.$root.$data.logOut = this.logOut
    document.title = "STCM";
    if(localStorage.getItem('loggedIn') != null){
      this.$root.$data.authToken = localStorage.getItem('authToken');
      this.checkLogin()
    }
    else{
      this.$root.$data.loggedIn = false;
      this.$root.$data.authToken = ""
      this.$router.push({ path: '/login' })
    }
  },
  methods: {
    checkLogin: async function(){
      const request = new Request(
      "http://127.0.0.1:5000/auth/userinfo",
        {
            method: "POST",
            mode: "cors",
            cache: "default",
            headers: {'Content-Type': 'application/json', 'Authentication': this.$root.$data.authToken},
            body: JSON.stringify({})
        }
      );
      const response = await fetch(request);
      const data = await response.json();
      if(data.username == undefined){
        this.logOut()
      }
    },
    logOut: function(){
      this.$root.$data.loggedIn = false
      this.$root.$data.authToken = null
      localStorage.clear()
      this.$router.push({ path: '/login' })
    }
  }
// created: async function(){
//         const gResponse = await fetch("http://127.0.0.1:5000/lookup?stock=App");
//         const gObject = await gResponse.json();
//         this.flaskGreeting = gObject.data;
// }
}
</script>

<style lang="scss">
@import "~bulma/sass/utilities/_all";
$stcm: rgb(165, 28, 48);
$stcm-invert: findColorInvert($stcm);


$colors: (
    "primary": ($stcm, $stcm-invert),
);

// Import Bulma and Buefy styles
@import "~bulma";
@import "~buefy/src/scss/buefy";

</style>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
