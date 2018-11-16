const state = {
  liveDataStream_IMU: [],
  liveRawStream_IMU: [],
  capturedDataStream_IMU: {},
  recentDataStream_IMU: [],
  capturing_IMU: false,
  headNames_IMU: [
    'AccX',
    'AccY',
    'AccZ',
    'GyrX',
    'GyrY',
    'GyrZ',
    'MagX',
    'MagY',
    'MagZ'
  ],
  lastPredictDataStream_IMU: [],
  lastPredictHistory_IMU: []
}

const mutations = {
  // socket connection
  START_CAPTURE_IMU: state => {
    console.log('START capturing...')
    state.capturing_IMU = true
  },
  STOP_CAPTURE_IMU: state => {
    console.log('STOP capturing ;;;')
    state.capturing_IMU = false
  },
  SAVE_CAPTURE_IMU: (state, name) => {
    if (state.recentDataStream_IMU.length === 0) {
      return
    }
    console.log('SAVE capturing...')
    let i = 1
    while (name in state.capturedDataStream_IMU) {
      name = name.split('.')[0] + '.' + i++
    }
    console.log(name, state.recentDataStream_IMU.length)
    state.capturedDataStream_IMU[name] = state.recentDataStream_IMU
    state.recentDataStream_IMU = []
  },
  RENAME_CAPTURE: (state, {
    oldname,
    newname
  }) => {
    console.log('SAVE capturing...')
    state.capturedDataStream_IMU[newname] = state.capturedDataStream_IMU[oldname]
    delete state.capturedDataStream_IMU[oldname]
  },
  CLEAR_CAPTURE_IMU: state => {
    console.log('CLEAR capturing...')
    state.capturing_IMU = false
    state.recentDataStream_IMU = []
    global.vm.$forceUpdate()
  },
  IMPORT_CAPTURE_IMU: (state, newStream) => {
    console.log('IMPORT capturing_IMU...')
    state.capturedDataStream_IMU = newStream
  },
  REMOVE_CAPTURE_IMU: (state, name) => {
    console.log('REMOVE capturing_IMU...')
    delete state.capturedDataStream_IMU[name]
  },
  // socket connection
  SOCKET_LIVEDATAIMU: (
    state, [payload]) => {
    if (state.liveDataStream_IMU.length < 20) {
      state.liveDataStream_IMU.push(payload.msg)
      state.liveRawStream_IMU.push(payload.ori)
    } else {
      state.liveDataStream_IMU.shift()
      state.liveDataStream_IMU.push(payload.msg)
      state.liveRawStream_IMU.shift()
      state.liveRawStream_IMU.push(payload.ori)
    }
    if (state.capturing_IMU) {
      state.recentDataStream_IMU.push(payload.msg)
    }
  },
  SOCKET_PREDICT_RESULT: (
    state, [payload]) => {
    console.log('PREDICTED', payload)
    if (state.lastPredictHistory_IMU.length < 5) {
      state.lastPredictHistory_IMU.unshift(payload)
    } else {
      state.lastPredictHistory_IMU.pop()
      state.lastPredictHistory_IMU.unshift(payload)
    }
  },
  SOCKET_LIVEDATACHANGE: (
    state, [payload]) => {
    // console.log(payload.msg)
    // if (payload.msg.length === 20) {
    //   while (state.liveDataStream_IMU.length > 0) {
    //     state.liveDataStream_IMU.shift()
    //   }
    //   for (let i = 0; i < 20; i++) {
    //     state.liveDataStream_IMU.push(payload.msg[i])
    //   }
    // }
    // if (state.capturing_IMU) {
    //   state.recentDataStream_IMU = payload.msg
    // }
  }
}

const actions = {
  manualPredictIMU: ({
    state
  }, payload) => {
    state.lastPredictDataStream_IMU = payload.slice()
    let mapped = payload.map(d => [...d[1].slice(0, 3), ...d[2].slice(0, 3), ...d[3].slice(0, 3), ...d[4].slice(0, 3), ...d[5].slice(0, 3)])
    console.log('predict')
    global.vm.$socket.emit('predict', mapped)
  }
}

const getters = {
  getDataAllIMU: state => state.liveDataStream_IMU,
  getDataRawIMU: state => state.liveRawStream_IMU,
  getIMU: state => i => state.liveDataStream_IMU.map(d => d[i]),
  getIMUAxis: state => (i, j) => state.liveDataStream_IMU.map(d => d[i][j]),
  getHeadNamesIMU: state => state.headNames_IMU,
  getCapturedDataStreamIMU: state => state.capturedDataStream_IMU,
  getRecentDataStreamIMU: state => state.recentDataStream_IMU,
  getRecentDataStreamSizeIMU: state => state.recentDataStream_IMU.length,
  isCapturingIMU: state => state.capturing_IMU,
  getLastPredictDataStreamIMU: state => state.lastPredictDataStream_IMU,
  getLastPredictHistoryIMU: state => state.lastPredictHistory_IMU
}

const module = {
  state,
  getters,
  mutations,
  actions
}

export default module
