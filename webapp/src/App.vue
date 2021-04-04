<template>
  <div id="app">
    <NavBar></NavBar>
    <br />
    <br />
    <StockSearch></StockSearch>
  </div>
</template>

<script>
// import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import NavBar from './components/NavBar.vue'
import StockSearch from './components/StockSearch.vue'

Vue.use(Buefy);

export default {
  name: 'App',
  components: {
    NavBar,
    StockSearch
  },
  data: function(){
    return {
        greeting: 'Hello, Vue!',
        flaskGreeting: ''
    }
},
// created: async function(){
//         const gResponse = await fetch("http://127.0.0.1:5000/lookup?stock=App");
//         const gObject = await gResponse.json();
//         this.flaskGreeting = gObject.data;
// }
}
</script>

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
