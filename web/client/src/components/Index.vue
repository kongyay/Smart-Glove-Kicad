<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <live-data-sheet :data-stream='dataStream'></live-data-sheet>
    </v-slide-y-transition>

    <v-layout row wrap>

      <v-btn color="secondary" @click='goLive()'>LIVE</v-btn>
      <v-btn color="secondary" @click='goNone()'>NONE</v-btn>

      <v-badge v-for='(value,i) in getCapturedDataStream' :key='i' overlap color="red">
        <v-btn slot="badge" @click='removeName(i)' flat icon dark small>X</v-btn>

        <v-btn @click='goName(i)' @dblclick="rename(i)" :class="{'green': selectedName===i}">
          {{i}}
        </v-btn>
      </v-badge>
    </v-layout>

    <v-layout row>
      <v-progress-linear :color="isCapturing? 'success':'info'" :value="saveDelayPercent"></v-progress-linear>
    </v-layout>

    <v-layout row>
      <v-text-field label="Gesture Name" solo v-model="saveName" ref='nameField' :rules="nameRules"></v-text-field>
      <v-spacer></v-spacer>
      <v-btn v-if='!isCapturing && !autoSave' color="info" @click='startAuto()'>Auto</v-btn>
      <v-btn v-if='!isCapturing && !autoSave' color="info" @click='startCapture()'>Start</v-btn>
      <v-btn v-else-if='!isCooldown' color="warning" @click='stopCapture()'>Stop</v-btn>
      <v-btn color="success" @click='saveCapture()'>Save</v-btn>
      <v-btn color="error" @click='clearCapture()'>Clear</v-btn>
    </v-layout>

    <v-layout row>
      <v-btn color="primary" @click='goPredict()'>PREDICT!</v-btn>
      <v-btn color="success" @click='resample()'>Resample</v-btn>
    </v-layout>

    <import-box></import-box>
    <export-box></export-box>

  </v-container>
</template>

<script>
import {mapGetters, mapMutations, mapActions} from 'vuex'
import LiveDataSheet from './LiveDataSheet.vue'
import ExportBox from './ExportBox.vue'
import ImportBox from './ImportBox.vue'

export default {
  data () {
    return {
      dataStream: [],
      saveName: 'test',
      nameRules: [v => !!v || 'Name is required', v => v.split('.').length < 3 || 'Must contain 0-1 dot.'],
      selectedName: '',
      autoSave: false,
      isCooldown: false,
      saveDelay: 2000,
      saveDelayPercent: 0,
      timer: null,
      timerCurrent: 0
    }
  },
  computed: {
    ...mapGetters(['getDataAll', 'isCapturing', 'getCaptureSize', 'getRecentDataStream', 'getRecentDataStreamSize', 'getCapturedDataStream', 'getLastPredictDataStream'])
  },
  methods: {
    ...mapMutations(['START_CAPTURE', 'STOP_CAPTURE', 'SAVE_CAPTURE', 'CLEAR_CAPTURE', 'REMOVE_CAPTURE', 'RENAME_CAPTURE']),
    ...mapActions(['manualPredict']),
    goLive () {
      this.dataStream = this.getDataAll
    },
    goNone () {
      this.dataStream = []
    },
    goName (name) {
      this.selectedName = name
      this.dataStream = this.getCapturedDataStream[name]
    },
    removeName (name) {
      this.REMOVE_CAPTURE(name)
      global.vm.$forceUpdate()
    },
    startAuto () {
      this.autoSave = true
      this.startCapture()
    },
    startCapture () {
      this.dataStream = this.getRecentDataStream
      this.START_CAPTURE()
    },
    stopCapture () {
      this.autoSave = false
      clearInterval(this.timer)
      this.STOP_CAPTURE()
    },
    clearCapture () {
      this.CLEAR_CAPTURE()
      this.dataStream = this.getRecentDataStream
    },
    saveCapture () {
      this.STOP_CAPTURE()
      if (this.$refs.nameField.validate()) {
        this.SAVE_CAPTURE(this.saveName)
        global.vm.$forceUpdate()
      }
    },
    goPredict () {
      this.dataStream = this.getLastPredictDataStream
      this.manualPredict()
    },
    rename (oldname) {
      let newname = prompt('Please enter new name:', '')
      if (newname !== null && newname !== '') {
        this.RENAME_CAPTURE({oldname: oldname, newname: newname})
      }
    },
    resample () {
      let mapped = {}
      for (const key in this.getCapturedDataStream) {
        let ges = this.getCapturedDataStream[key]
        mapped[key] = ges[0].map((col, i) => ges.map(row => row[i]))
      }
      this.$socket.emit('resample', mapped, 20)
    }
  },
  watch: {
    getRecentDataStreamSize (val, old) {
      if (val >= this.getCaptureSize && this.autoSave) {
        this.STOP_CAPTURE()
        this.saveCapture(this.saveName)
        this.isCooldown = true
        console.log('what')
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
  components: {LiveDataSheet, ExportBox, ImportBox}
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
