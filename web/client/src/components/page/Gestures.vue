<template>
  <v-container grid-list-md  fluid>
    <v-layout row wrap>
      <v-flex class='gestureTab'>
        Gesture
        <v-layout row wrap>
          <v-flex xs12 md3 v-for="ges in getChoiceGesture" :key="ges.name">
            <gesture-box  :gesture='ges' :selected="getPoolGesture.map(g=>g.name).indexOf(ges.name)<0"></gesture-box>
          </v-flex>
        </v-layout>
        <v-btn block outline color="black" style="border-style: dashed" @click="addGesture"><b>+</b> Create Gesture</v-btn>
      </v-flex>
    </v-layout>

    <ga-combo v-for='(ga,i) in getCurrentProfile.gestures_actions' :key='i' :ga="ga" :choiceGesture="[ga.gesture].concat(getPoolGesture)" :choiceAction="getChoiceAction" :profileName="getCurrentProfile.name"></ga-combo>
    <v-btn v-if='getPoolGesture.length>0' block outline color="black" style="border-style: dashed; height: 50px" @click="addGA"><b>+ Add new Gesture->Action</b></v-btn>

  </v-container>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import GestureBox from '../GestureBox.vue'
import HistoryBox from '../HistoryBox.vue'
import GaCombo from '../GaCombo.vue'

export default {
  data () {
    return {
      poolAction: [],
      activeG: [],
      activeAction: []
    }
  },
  computed: {
    ...mapGetters(['getCurrentProfile', 'getChoiceGesture', 'getPoolGesture', 'getChoiceAction'])
  },
  methods: {
    ...mapMutations(['ADD_GESTURE', 'REMOVE_GESTURE', 'ADD_GA', 'REMOVE_GA']),
    addGesture () {
      let newname = prompt('Please enter gesture name:', '')
      if (newname !== null && newname !== '') {
        this.ADD_GESTURE(newname)
      }
    },
    addGA () {
      this.ADD_GA()
    }
  },
  created () {

  },
  components: {
    GestureBox, HistoryBox, GaCombo
  }
}
</script>

<style scoped>
.gestureTab {
  background-color: rgba(235, 235, 255, 0.171)
}
.actionTab {
  background-color: rgba(255, 240, 251, 0.37)
}
</style>
