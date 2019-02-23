<template>
  <v-container>
    Predict History
    <v-btn v-if='getLastPredictHistoryIMU.length===0' block disabled>No History</v-btn>
    <v-layout row v-for='(val,i) in getLastPredictHistoryIMU' :key='"p"+i'>
      <v-btn block :large='i===0' :outline='i!=0' color="green">{{val}}</v-btn>
    </v-layout>

    Action History
    <v-btn v-if='getLastActionHistoryIMU.length===0' block disabled>No History</v-btn>

    <v-expansion-panel expand>
      <v-expansion-panel-content
        v-for='(act,i) in getLastActionHistoryIMU' :key='"a"+i' :value='i===0' :class="i===0 ? 'orange lighten-2':'white'"
      >
        <div slot="header">{{act.ga.gesture.name}} -> {{act.ga.action.name}}</div>
          <v-flex xs12>
          <v-card color="brown" class="white--text" >
            <v-layout>
              <v-flex xs2>
                <v-img
                  :src="act.ga.action.pic"
                  height="125px"
                  contain
                ></v-img>
              </v-flex>
              <v-flex xs10>
                <v-card-title primary-title>
                  <div>
                    <div class="headline">{{act.ga.gesture.name}} -> {{act.ga.action.name}}</div>
                    <code>{{act.result}}</code>
                  </div>
                </v-card-title>
              </v-flex>
            </v-layout>
          </v-card>
        </v-flex>
      </v-expansion-panel-content>
    </v-expansion-panel>

  </v-container>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  data () {
    return {

    }
  },
  computed: {
    ...mapGetters(['getLastPredictDataStreamIMU', 'getLastPredictHistoryIMU', 'getLastActionHistoryIMU', 'getChoicePose'])
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
