// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import Vuex from 'vuex'

import VueSocketio from 'vue-socket.io'
import socketio from 'socket.io-client'
import store from './store'
import axios from 'axios'

let host = '161.246.6.42'
Vue.use(Vuetify)
Vue.use(Vuex)
Vue.use(VueSocketio, socketio(`http://${host}:3000/web`), store)
axios.get(`http://${host}:3000/api`).then(response => console.log(response))

Vue.config.productionTip = false

/* eslint-disable no-new */
global.vm = new Vue({
  el: '#app',
  router,
  store,
  components: {
    App
  },
  template: '<App/>'
})
