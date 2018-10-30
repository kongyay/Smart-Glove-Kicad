import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Super from '@/components/Super'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'Index',
    component: Index
  }, {
    path: '/super',
    name: 'Super',
    component: Super
  }]
})
