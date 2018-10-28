// import axios from 'axios'

const state = {
  isConnected: false,
  liveDataStream: [],
  capturedDataStream: {},
  recentDataStream: [],
  capturing: false,
  headNames: ['AccX', 'AccY', 'AccZ', 'GyrX', 'GyrY', 'GyrZ', 'MagX', 'MagY', 'MagZ', 'โป้ง', 'ชี้', 'กลาง', 'นาง', 'ก้อย']
}

const mutations = {
  // socket connection
  START_CAPTURE: (state) => {
    console.log('START capturing...')
    state.capturing = true
  },
  STOP_CAPTURE: (state) => {
    console.log('STOP capturing ;;;')
    state.capturing = false
  },
  SAVE_CAPTURE: (state, name) => {
    console.log('SAVE capturing...')
    state.capturedDataStream[name] = state.recentDataStream
    state.recentDataStream = []
  },
  RENAME_CAPTURE: (state, {
    oldname,
    newname
  }) => {
    console.log('SAVE capturing...')
    state.capturedDataStream[newname] = state.capturedDataStream[oldname]
    delete state.capturedDataStream[oldname]
  },
  CLEAR_CAPTURE: (state) => {
    console.log('CLEAR capturing...')
    state.recentDataStream = []
    global.vm.$forceUpdate()
  },
  IMPORT_CAPTURE: (state, newStream) => {
    console.log('IMPORT capturing...')
    state.capturedDataStream = newStream
  },
  REMOVE_CAPTURE: (state, name) => {
    console.log('REMOVE capturing...')
    delete state.capturedDataStream[name]
  },
  SOCKET_CONNECT: (state) => {
    console.log('connected')
    state.isConnected = true
  },
  SOCKET_DISCONNECT: (state) => {
    console.log('disconnected')
    state.isConnected = false
  },
  SOCKET_LIVEDATA: (state, [payload]) => {
    // console.log(payload)
    if (state.liveDataStream.length < 15) {
      state.liveDataStream.push(payload.msg)
    } else {
      // for (let i = 0; i < 14; i++) {
      //   let diff = Math.abs(payload.msg[i] - state.liveDataStream[14][i])
      //   if (i === 13 && diff < 50) {
      //     console.log('Prepare to Predict...', payload.msg[i], state.liveDataStream[14][i])
      //     axios
      //       .get(`http://161.246.6.41:3000/predict/all`, {
      //         params: {
      //           data: JSON.stringify(payload.msg)
      //         }
      //       })
      //       .then(response => console.log('PREDICTED', response))
      //       .catch(error => console.log(error.response))
      //     break
      //   } else if (diff > 50) {
      //     break
      //   }
      // }

      state.liveDataStream.shift()
      state.liveDataStream.push(payload.msg)
    }
    if (state.capturing) {
      state.recentDataStream.push(payload.msg)
    }
  },
  SOCKET_RESAMPLED: (state, [payload]) => {
    console.log(payload)
    let mapped = {}
    for (const key in payload) {
      let ges = payload[key]
      mapped[key] = ges[0].map((col, i) => ges.map(row => row[i]))
    }
    state.capturedDataStream = mapped
  }
}

const actions = {}

const getters = {
  getConnected: state => state.isConnected,
  getDataAll: state => state.liveDataStream,
  getDataAcc: state => state.liveDataStream.map((d) => d.slice(0, 3)),
  getDataGyro: state => state.liveDataStream.map((d) => d.slice(3, 6)),
  getDataMag: state => state.liveDataStream.map((d) => d.slice(6, 9)),
  getDataFlex: state => state.liveDataStream.map((d) => d.slice(9, 14)),
  isCapturing: state => state.capturing,
  getRecentDataStream: state => state.recentDataStream,
  getCapturedDataStream: state => state.capturedDataStream,
  getHeadNames: state => state.headNames
}
export default {
  namespaced: true,
  mutations,
  getters,
  state,
  actions
}
