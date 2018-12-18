const state = {
  isConnected: false,
  isLoaded: false,
  profiles: [{name: 'NONE'}],
  currentProfile: {name: 'NONE'},
  choicePose: [],
  choiceAction: [],
  choiceGesture: []
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
    console.log('ADD Gesture...')
    let newGA = {
      gesture: {
        name: payload,
        poses: [state.choicePose[0]]
      },
      action: state.choiceAction[0],
      args: ['', '']
    }
    state.currentProfile.gestures_actions.push(newGA)
  },
  REMOVE_GESTURE: (
    state, payload) => {
    console.log('REMOVE Gesture...')
    for (let i = 0; i < state.currentProfile.gestures_actions.length; i++) {
      if (state.currentProfile.gestures_actions[i].gesture.name === payload) {
        state.currentProfile.gestures_actions.splice(i, 1)
        break
      }
    }
  },
  SOCKET_PROFILES_RESULT: (
    state, [payload]) => {
    console.log('FETCH Profile...', payload)
    state.profiles = payload
    state.isLoaded = true
    if (state.currentProfile.name === 'NONE') {
      state.currentProfile = state.profiles.find(p => p.name === 'Default')
    }
  },
  SOCKET_CHOICES_RESULT: (
    state, [payload]) => {
    console.log('FETCH Choices...', payload)
    state.choicePose = payload[0]
    state.choiceAction = payload[1]
    state.choiceGesture = payload[2]
  },
  SOCKET_SAVE_GESTURE_RESULT: (
    state, [payload]) => {
    console.log('Save Gesture Result:', payload)
  },
  SOCKET_REMOVE_GESTURE_RESULT: (
    state, [payload]) => {
    console.log('Remove Gesture Result:', payload)
  }
}

const actions = {
  fetchProfiles: ({
    state
  }, payload) => {

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
  getChoiceGesture: state => state.choiceGesture
}

const module = {
  state,
  getters,
  mutations,
  actions
}

export default module
