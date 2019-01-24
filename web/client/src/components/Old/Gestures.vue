<template>
  <v-container fluid>
    <div v-if="getCurrentProfile.name !== 'NONE'">
      <gesture-box v-for="(ges,i) in getCurrentProfile.gestures_actions" :key=i :profile_name='getCurrentProfile.name' :gestureAction="ges"></gesture-box>
      <v-btn color='secondary' @click='addGesture'>Add</v-btn>
    </div>
    <history-box></history-box>
  </v-container>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import GestureBox from '../GestureBox.vue'
import HistoryBox from '../HistoryBox.vue'

export default {
  data () {
    return {

    }
  },
  computed: {
    ...mapGetters(['getCurrentProfile', 'getChoicePose', 'getChoiceAction'])
  },
  methods: {
    ...mapMutations(['ADD_GESTURE']),
    addGesture () {
      console.log('ADD Gesture')
      let newname = prompt('Please enter gesture name:', '')
      if (newname !== null && newname !== '') {
        this.ADD_GESTURE(newname)
      }
    }
  },
  components: {
    GestureBox, HistoryBox
  }
}
</script>
