<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <live-data-sheet :data-stream='dataStream'></live-data-sheet>
    </v-slide-y-transition>

    <v-layout row wrap>
      <v-btn color="secondary" @click='goLive()'>LIVE</v-btn>
      <v-btn color="secondary" @click='goNone()'>NONE</v-btn>
    </v-layout>

    <v-layout row>
      <v-progress-linear :color="isCapturing? 'success':'info'" :value="saveDelayPercent"></v-progress-linear>
    </v-layout>

    <v-layout row >
      <v-btn v-if='!isCapturing && !autoPredict' color="primary" @click='doAutoPredict()'>AUTO PREDICT!</v-btn>
      <v-btn v-else :disabled='isCooldown'  color="warning" @click='stopCapture()'>Stop</v-btn>
      <v-btn color="primary" @click='doPredict(getDataAll)'>PREDICT!</v-btn>
      <v-btn color="error" @click='clearCapture()'>Clear</v-btn>
    </v-layout>

    <v-layout row v-for='(val,i) in getLastPredictHistory' :key=i>
      <v-btn block :small='i!=0' :outline='i!=0' color="green">{{gestureName[parseInt(val)-1]}}</v-btn>
    </v-layout>

  </v-container>
</template>

<script>
import {mapGetters, mapMutations, mapActions} from 'vuex'
import LiveDataSheet from '../LiveDataSheet.vue'
export default {
  data () {
    return {
      gestureName: ['Left', 'Right', 'Up', 'Comeon', 'Idle'],
      dataStream: [],
      autoPredict: false,
      isCooldown: false,
      saveDelay: 2000,
      saveDelayPercent: 0,
      timer: null,
      timerCurrent: 0
    }
  },
  computed: {
    ...mapGetters(['getDataAll', 'isCapturing', 'getCaptureSize', 'getRecentDataStream', 'getRecentDataStreamSize', 'getCapturedDataStream', 'getLastPredictDataStream', 'getLastPredictHistory'])
  },
  methods: {
    ...mapMutations(['START_CAPTURE', 'STOP_CAPTURE', 'CLEAR_CAPTURE']),
    ...mapActions(['manualPredict']),
    goLive () {
      this.dataStream = this.getDataAll
    },
    goNone () {
      this.dataStream = []
    },
    startCapture () {
      this.dataStream = this.getRecentDataStream
      this.START_CAPTURE()
    },
    stopCapture () {
      this.autoSave = false
      this.autoPredict = false
      clearInterval(this.timer)
      this.STOP_CAPTURE()
    },
    clearCapture () {
      this.CLEAR_CAPTURE()
      this.dataStream = this.getRecentDataStream
    },
    doPredict (datas) {
      this.manualPredict(datas)
      this.dataStream = this.getLastPredictDataStream
    },
    doAutoPredict () {
      this.autoPredict = true
      this.startCapture()
    }
  },
  watch: {
    getRecentDataStreamSize (val, old) {
      if (val >= this.getCaptureSize && this.autoPredict) {
        this.STOP_CAPTURE()
        this.doPredict(this.getRecentDataStream)
        this.CLEAR_CAPTURE()
        this.isCooldown = true
        clearInterval(this.timer)
        this.timer = setInterval(() => {
          this.timerCurrent += 1
          this.saveDelayPercent = 90 - (this.timerCurrent / 10 * 100)
          if (this.timerCurrent >= 10) {
            this.timerCurrent = 0
            this.isCooldown = false
            this.startCapture()
            clearInterval(this.timer)
          }
        }, this.saveDelay / 10)
      } else if (val < this.getCaptureSize && val > 0) {
        this.saveDelayPercent = (val + 1) / this.getCaptureSize * 100
      }
    }
  },
  mounted () {
    this.dataStream = this.getDataAll
  },
  components: {LiveDataSheet}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.green {
  background-color: #41b883;
}
</style>
