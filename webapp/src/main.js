import Vue from 'vue'
import App from './App.vue'

var sourceOfTruth = {
  loggedIn: false,
  authToken: null
}

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  data: sourceOfTruth
}).$mount('#app')

