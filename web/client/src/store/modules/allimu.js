const state = {
  liveDataStream_IMU: [],
  capturedDataStream_IMU: {},
  recentDataStream_IMU: [],
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
  ]
}

const mutations = {
  // socket connection
  SOCKET_LIVEDATAIMU: (state, [payload]) => {
    // console.log(payload)
    if (state.liveDataStream_IMU.length < state.captureSize) {
      state.liveDataStream_IMU.push(payload.msg)
    } else {
      state.liveDataStream_IMU.shift()
      state.liveDataStream_IMU.push(payload.msg)
    }
    if (state.capturing) {
      state.recentDataStream_IMU.push(payload.msg)
    }
  }
}

const actions = {

}

const getters = {
  getDataAllIMU: state => i => state.liveDataStream_IMU,
  getIMU: state => i => state.liveDataStream_IMU.map(d => d[i]),
  getIMUAxis: state => (i, j) => state.liveDataStream_IMU.map(d => d[i][j]),
  getHeadNamesIMU: state => state.headNames_IMU
}

const module = {
  state,
  getters,
  mutations,
  actions
}

export default module
