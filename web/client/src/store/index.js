import Vue from 'vue'
import Vuex from 'vuex'

import flex from './modules/flexStore'
import allimu from './modules/allimuStore'
import user from './modules/userStore'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

// export default function (/* { ssrContext } */) {
//   const Store = new Vuex.Store(music)

//   return Store
// }
export default new Vuex.Store({
  modules: {
    flex,
    allimu,
    user
  }
})
