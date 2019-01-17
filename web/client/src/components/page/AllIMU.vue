<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <live-data-sheet :data-stream='dataStream' :dataBG='dataBG'></live-data-sheet>
    </v-slide-y-transition>

    <v-layout row wrap>
      <v-btn outline small round>MAIN</v-btn>
      <v-btn color="secondary" @click='goNone(true)'>NONE</v-btn>
      <v-btn color="secondary" @click.left='goLive(true)' @click.right='goLive(false)'>LIVE</v-btn>
    </v-layout>

    <v-layout row wrap>
      <v-btn outline small round>BG</v-btn>
      <v-btn color="secondary" @click='goNone(false)'>NONE</v-btn>
      <v-btn color="secondary" @click.left='goRaw(false)' @click.right='goRaw(true)'>RAW</v-btn>

      <v-badge v-for='(value,i) in getCapturedDataStreamIMU' :key='i' overlap color="red">
        <v-btn slot="badge" @click='removeName(i)' flat icon dark small>X</v-btn>

        <v-btn @click.left='goName(i)' @dblclick="rename(i)" @click.right='goName(i,true)' :class="{'green': selectedName===i}">
          {{i}}
        </v-btn>
      </v-badge>
    </v-layout>

    <v-layout row>
      <v-progress-linear :color="isCapturingIMU? 'success':'info'" :value="saveDelayPercent"></v-progress-linear>
    </v-layout>

    <v-layout row>
      <v-text-field label="Gesture Name" solo v-model="saveName" ref='nameField' :rules="nameRules"></v-text-field>
      <v-spacer></v-spacer>
      <v-btn v-if='!isCapturingIMU && !autoSave' color="info" @click='startAuto()'>Auto</v-btn>
      <v-btn v-if='!isCapturingIMU && !autoSave' color="info" @click='startCapture()'>Start</v-btn>
      <v-btn v-else :disabled='isCooldown' color="warning" @click='stopCapture()'>Stop</v-btn>
      <v-btn color="success" @click='saveCapture()'>Save</v-btn>
      <v-btn color="error" @click='clearCapture()'>Clear</v-btn>
    </v-layout>

    <v-layout row >
      <v-btn v-if='!isCapturingIMU && !autoPredict' color="primary" @click='doAutoPredict()'>AUTO PREDICT!</v-btn>
      <v-btn v-else :disabled='isCooldown'  color="warning" @click='stopCapture()'>Stop</v-btn>
      <v-btn color="primary" @click='doPredict(getDataAllIMU)'>PREDICT!</v-btn>
      <v-btn color="error" @click='clearCapture()'>Clear</v-btn>
    </v-layout>

    <history-box></history-box>

    <import-box></import-box>
    <export-box></export-box>

  </v-container>
</template>

<script>
import {mapGetters, mapMutations, mapActions} from 'vuex'
import LiveDataSheet from '../LiveDataSheet.vue'
import ExportBox from '../ExportBox.vue'
import ImportBox from '../ImportBox.vue'
import HistoryBox from '../HistoryBox.vue'

export default {
  data () {
    return {
      gestureName: ['กำ', 'แบ', 'รัก', 'ชูสองนิ้ว', 'ไขว้', 'ก', 'ข', 'ค', 'ง'],
      dataStream: [],
      dataBG: [],
      saveName: 'test',
      nameRules: [v => !!v || 'Name is required', v => v.split('.').length < 3 || 'Must contain 0-1 dot.'],
      selectedName: '',
      autoSave: false,
      autoPredict: false,
      isCooldown: false,
      saveDelay: 2000,
      saveDelayPercent: 0,
      timer: null,
      timerCurrent: 0
    }
  },
  computed: {
    ...mapGetters(['getDataAllIMU', 'getDataRawIMU', 'isCapturingIMU', 'getCaptureSize', 'getRecentDataStreamIMU', 'getRecentDataStreamSizeIMU', 'getCapturedDataStreamIMU', 'getLastPredictDataStreamIMU'])
  },
  methods: {
    ...mapMutations(['START_CAPTURE_IMU', 'STOP_CAPTURE_IMU', 'SAVE_CAPTURE_IMU', 'CLEAR_CAPTURE_IMU', 'REMOVE_CAPTURE_IMU', 'RENAME_CAPTURE_IMU']),
    ...mapActions(['manualPredictIMU']),
    goLive (main = true) {
      main ? this.dataStream = this.getDataAllIMU : this.dataBG = this.getDataAllIMU
    },
    goRaw (main = false) {
      main ? this.dataStream = this.getDataRawIMU : this.dataBG = this.getDataRawIMU
    },
    goNone (main = true) {
      main ? this.dataStream = [] : this.dataBG = []
    },
    goName (name, main = false) {
      this.selectedName = name
      main ? this.dataStream = [] : this.dataBG = this.getCapturedDataStreamIMU[name]
    },
    removeName (name) {
      this.REMOVE_CAPTURE_IMU(name)
      global.vm.$forceUpdate()
    },
    startAuto () {
      this.autoSave = true
      this.startCapture()
    },
    startCapture () {
      this.dataStream = this.getRecentDataStreamIMU
      this.START_CAPTURE_IMU()
    },
    stopCapture () {
      this.autoSave = false
      this.autoPredict = false
      clearInterval(this.timer)
      this.STOP_CAPTURE_IMU()
    },
    clearCapture () {
      this.CLEAR_CAPTURE_IMU()
      this.dataStream = this.getRecentDataStreamIMU
    },
    saveCapture () {
      this.STOP_CAPTURE_IMU()
      if (this.$refs.nameField.validate()) {
        this.SAVE_CAPTURE_IMU(this.saveName)
        global.vm.$forceUpdate()
      }
    },
    rename (oldname) {
      let newname = prompt('Please enter new name:', '')
      if (newname !== null && newname !== '') {
        this.RENAME_CAPTURE_IMU({oldname: oldname, newname: newname})
      }
    },
    doPredict (datas) {
      this.manualPredictIMU(datas)
      this.dataStream = this.getLastPredictDataStreamIMU
    },
    doAutoPredict () {
      this.autoPredict = true
      this.startCapture()
    }
  },
  mounted () {
    // this.dataStream = this.getDataAll
  },
  watch: {
    getRecentDataStreamSizeIMU (val, old) {
      if (val >= this.getCaptureSize && (this.autoSave || this.autoPredict)) {
        this.STOP_CAPTURE_IMU()
        if (this.autoSave) {
          this.dataStream = this.getRecentDataStreamIMU
          this.saveCapture(this.saveName)
        } else {
          this.doPredict(this.getRecentDataStreamIMU)
          this.dataStream = this.getLastPredictDataStreamIMU
          this.CLEAR_CAPTURE_IMU()
        }

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
  components: {LiveDataSheet, ExportBox, ImportBox, HistoryBox}
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
