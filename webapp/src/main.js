import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Login from './components/Login.vue'
import StockSearch from './components/StockSearch.vue'
import Voting from './components/Voting.vue'

Vue.use(VueRouter)

const routes = [
  { path: '', redirect: '/login'},
  { path: '/login', component: Login, name: Login},
  { path: '/search', component: StockSearch, name: StockSearch},
  { path: '/voting', component: Voting, name: Voting},
  { path: '*', redirect: '/login'}
]

// note: I'm gonna put the voting component inside a user page when we get there - Gordon

const router = new VueRouter({
  mode: 'history',
  routes: routes,  // short for `routes: routes`
  scrollBehavior () {

    return { x: 0, y: 0 }
}
})

var sourceOfTruth = {
  loggedIn: false,
  authToken: null
}

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  data: sourceOfTruth
}).$mount('#app')
