import axios from 'axios'

const state = {
  isConnected: false,
  liveDataStream: [],
  capturedDataStream: {},
  recentDataStream: [],
  lastPredictDataStream: [],
  capturing: false,
  captureSize: 20,
  headNames: [
    'AccX',
    'AccY',
    'AccZ',
    'GyrX',
    'GyrY',
    'GyrZ',
    'MagX',
    'MagY',
    'MagZ',
    'โป้ง',
    'ชี้',
    'กลาง',
    'นาง',
    'ก้อย'
  ]
}

const mutations = {
  // socket connection
  START_CAPTURE: state => {
    console.log('START capturing...')
    state.capturing = true
  },
  STOP_CAPTURE: state => {
    console.log('STOP capturing ;;;')
    state.capturing = false
  },
  SAVE_CAPTURE: (state, name) => {
    if (state.recentDataStream.length === 0) {
      return
    }
    console.log('SAVE capturing...')
    let i = 1
    while (name in state.capturedDataStream) {
      name = name.split('.')[0] + '.' + i++
    }
    console.log(name, state.recentDataStream.length)
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
  CLEAR_CAPTURE: state => {
    console.log('CLEAR capturing...')
    state.capturing = false
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
  SOCKET_CONNECT: state => {
    console.log('connected')
    state.isConnected = true
  },
  SOCKET_DISCONNECT: state => {
    console.log('disconnected')
    state.isConnected = false
  },
  SOCKET_LIVEDATA: (state, [payload]) => {
    // console.log(payload)
    if (state.liveDataStream.length < state.captureSize) {
      state.liveDataStream.push(payload.msg)
    } else {
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

const actions = {
  manualPredict: ({
    state
  }) => {
    state.lastPredictDataStream = state.liveDataStream.slice()
    axios
      .get(`http://161.246.6.41:3000/predict/moveimu`, {
        params: {
          data: JSON.stringify(state.liveDataStream)
        }
      })
      .then(response => console.log('PREDICTED', response))
      .catch(error => console.log(error.response))
  }
}

const getters = {
  getConnected: state => state.isConnected,
  getDataAll: state => state.liveDataStream,
  getDataAcc: state => state.liveDataStream.map(d => d.slice(0, 3)),
  getDataGyro: state => state.liveDataStream.map(d => d.slice(3, 6)),
  getDataMag: state => state.liveDataStream.map(d => d.slice(6, 9)),
  getDataFlex: state => state.liveDataStream.map(d => d.slice(9, 14)),
  isCapturing: state => state.capturing,
  getCaptureSize: state => state.captureSize,
  getRecentDataStream: state => state.recentDataStream,
  getRecentDataStreamSize: state => state.recentDataStream.length,
  getCapturedDataStream: state => state.capturedDataStream,
  getLastPredictDataStream: state => state.lastPredictDataStream,
  getHeadNames: state => state.headNames
}
export default {
  namespaced: true,
  mutations,
  getters,
  state,
  actions
}
