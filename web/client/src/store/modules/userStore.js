const state = {
  isConnected: false,
  isLoaded: false,
  profiles: [{name: 'NONE'}],
  currentProfile: {name: 'NONE'},
  choicePose: [],
  choiceAction: [],
  choiceGesture: [],
  connections: [],
  snackbarText: '',
  snackbarEnabled: false
}

const mutations = {
  // socket connection
  SOCKET_CONNECT: state => {
    console.log('connected')
    state.isConnected = true
    global.vm.$socket.emit('profiles')
    global.vm.$socket.emit('choices')
  },
  SOCKET_DISCONNECT: state => {
    console.log('disconnected')
    state.isConnected = false
    state.isLoaded = false
  },
  ADD_PROFILE: (
    state, payload) => {
    console.log('ADD Profile...')
    state.profiles.push(payload)
  },
  REMOVE_PROFILE: (
    state, payload) => {
    console.log('REMOVE Profile...')
    // REMOVE HERE
  },
  CHANGE_PROFILE: (
    state, payload) => {
    console.log('CHANGE Profile...')
    state.currentProfile = state.profiles.find(p => p.name === payload)
  },
  ADD_GESTURE: (
    state, payload) => {
    console.log('ADD Gesture...', payload)
    let newG =
      {
        name: payload,
        poses: [state.choicePose[0]]
      }

    state.choiceGesture.push(newG)
    global.vm.$socket.emit('saveGesture', newG)
  },
  REMOVE_GESTURE: (
    state, payload) => {
    console.log('REMOVE Gesture...')
    for (let i = 0; i < state.choiceGesture.length; i++) {
      if (state.choiceGesture[i].name === payload) {
        state.choiceGesture.splice(i, 1)
        return
      }
    }
  },
  ADD_GA: (
    state) => {
    console.log('ADD GA...', getters)
    let existGesture = state.currentProfile.gestures_actions.map(x => x.gesture.name)
    let pool = state.choiceGesture.filter(g => existGesture.indexOf(g.name) < 0)
    let newGA = {
      gesture: pool[0],
      action: state.choiceAction[0],
      args: {}
    }
    state.currentProfile.gestures_actions.push(newGA)
    global.vm.$socket.emit('saveGA', state.currentProfile.name, newGA.gesture.name, newGA)
  },
  REMOVE_GA: (
    state, payload) => {
    console.log('REMOVE GA...')
    for (let i = 0; i < state.currentProfile.gestures_actions.length; i++) {
      if (state.currentProfile.gestures_actions[i].gesture.name === payload) {
        state.currentProfile.gestures_actions.splice(i, 1)
        return
      }
    }
  },
  SET_GA: (
    state, {name, newGA}) => {
    console.log('SET GA...', name)
    for (let i = 0; i < state.currentProfile.gestures_actions.length; i++) {
      if (state.currentProfile.gestures_actions[i].gesture.name === name) {
        state.currentProfile.gestures_actions[i] = newGA
        return
      }
    }
  },
  SOCKET_PROFILES_RESULT: (
    state, payload) => {
    console.log('FETCH Profile...', payload)
    state.profiles = payload
    state.isLoaded = true
    if (state.currentProfile.name === 'NONE') {
      state.currentProfile = state.profiles.find(p => p.name === 'Default')
    }
  },
  SOCKET_CHOICES_RESULT: (
    state, payload) => {
    console.log('FETCH Choices...', payload)
    state.choicePose = payload[0]
    state.choiceAction = payload[1]
    state.choiceGesture = payload[2]
  },
  SOCKET_SAVE_GESTURE_RESULT: (
    state, payload) => {
    console.log('Save Gesture Result:', payload)
    state.snackbarText = payload
    state.snackbarEnabled = true
  },
  SOCKET_REMOVE_GESTURE_RESULT: (
    state, payload) => {
    console.log('Remove Gesture Result:', payload)
    state.snackbarText = payload
    state.snackbarEnabled = true
  },
  SOCKET_GET_NW_RESULT: (
    state, payload) => {
    console.log('get nw', payload)
    state.connections = payload
  }
}

const actions = {
  showSnackbar: ({
    state
  }, payload) => {
    state.snackbarText = payload
    state.snackbarEnabled = true
  },
  hideSnackbar: ({
    state
  }) => {
    state.snackbarText = ''
    state.snackbarEnabled = false
  }
}

const getters = {
  getConnected: state => state.isConnected,
  getLoaded: state => state.isLoaded,
  getProfile: state => name => state.profiles[name],
  getCurrentProfile: state => state.currentProfile,
  getProfileList: state => state.profiles.map(d => d.name),
  getChoicePose: state => state.choicePose,
  getChoiceAction: state => state.choiceAction,
  getChoiceGesture: state => state.choiceGesture,
  getPoolGesture: state => {
    if (state.currentProfile.gestures_actions) {
      let existGesture = state.currentProfile.gestures_actions.map(x => x.gesture.name)
      return state.choiceGesture.filter(g => existGesture.indexOf(g.name) < 0)
    }
    return []
  },
  getConnection: state => state.connections
}

const module = {
  state,
  getters,
  mutations,
  actions
}

export default module
