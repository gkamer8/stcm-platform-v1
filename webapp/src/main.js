import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Login from './components/Login.vue'
import StockSearch from './components/StockSearch.vue'

Vue.use(VueRouter)

const routes = [
  { path: '', redirect: '/login'},
  { path: '/login', component: Login, name: Login},
  { path: '/search', component: StockSearch, name: StockSearch},
  { path: '*', redirect: '/login'}
]

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
