const state = {
  isConnected: false,
  dataset: []

}

const mutations = {
  // socket connection
  SOCKET_CONNECT: (state) => {
    console.log('connected')
    state.isConnected = true
  },
  SOCKET_DISCONNECT: (state) => {
    console.log('disconnected')
    state.isConnected = false
  },
  SOCKET_LIVEDATA: (state, [payload]) => {
    console.log(payload)
    if (state.dataset.length < 15) {
      state.dataset.push(payload.msg)
    } else {
      state.dataset.shift()
      state.dataset.push(payload.msg)
    }
  }
}

const actions = {}

const getters = {
  getConnected: state => state.isConnected,
  getDataAcc: state => state.dataset.map((d) => d.slice(0, 3)),
  getDataGyro: state => state.dataset.map((d) => d.slice(3, 6)),
  getDataMag: state => state.dataset.map((d) => d.slice(6, 9)),
  getDataFlex: state => state.dataset.map((d) => d.slice(9, 14))
}

export default {
  namespaced: true,
  mutations,
  getters,
  state,
  actions
}
