import axios from 'axios'

const state = {
  profiles: ['Default']
}

const mutations = {
  // socket connection
  ADD_PROFILE: (
    state, [payload]) => {
    console.log('ADD Profile...')
    state.profiles.push(payload)
  }
}

const actions = {
  fetchProfiles: ({
    state
  }, payload) => {
    axios
      .get(`http://169.254.1.1:3000/profiles`, {
        params: {
          username: {}
        }
      })
      .then(response => {
        console.log('PREDICTED', response.data)
      })
  }
}

const getters = {
  getProfiles: state => state.profiles
}

const module = {
  state,
  getters,
  mutations,
  actions
}

export default module
