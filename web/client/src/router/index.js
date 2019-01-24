import Vue from 'vue'
import Router from 'vue-router'
import Flex from '@/components/page/Flex'
import Predict from '@/components/page/Predict'
import Gestures from '@/components/page/GesturesDrag'
import AllImu from '@/components/page/AllImu'
import Settings from '@/components/page/Settings'
Vue.use(Router)

export default new Router({
  routes: [{
    path: '/',
    name: 'Index',
    component: AllImu
  }, {
    path: '/gestures',
    name: 'gestures',
    component: Gestures
  }, {
    path: '/allimu',
    name: 'allImu',
    component: AllImu
  }, {
    path: '/flex',
    name: 'Flex',
    component: Flex
  }, {
    path: '/predict',
    name: 'Predict',
    component: Predict
  }, {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }]
})
