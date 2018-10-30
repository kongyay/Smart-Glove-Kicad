import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/page/Index'
import AllIMU from '@/components/page/AllIMU'
import Predict from '@/components/page/Predict'

Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'Index',
    component: Index
  }, {
    path: '/allimu',
    name: 'AllIMU',
    component: AllIMU
  }, {
    path: '/predict',
    name: 'Predict',
    component: Predict
  }]
})
