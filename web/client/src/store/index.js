import Vue from 'vue'
import Vuex from 'vuex'

import glove from './modules/glove'
import allimu from './modules/allimu'

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
    glove,
    allimu
  }
})
