<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <live-data-sheet :data-stream='dataStream'></live-data-sheet>
    </v-slide-y-transition>

    <v-layout row wrap>
      <v-btn v-if='!isCapturing' color="info" @click='startCapture()'>Start</v-btn>
      <v-btn v-else color="warning" @click='STOP_CAPTURE()'>Stop</v-btn>
      <v-btn color="secondary" @click='goLive()'>LIVE</v-btn>
      <v-btn color="secondary" @click='goNone()'>NONE</v-btn>

      <v-badge v-for='(value,i) in getCapturedDataStream' :key='i' overlap color="red">
        <v-btn slot="badge" @click='removeName(i)' flat icon dark small>X</v-btn>

        <v-btn @click='goName(i)' @dblclick="rename(i)" :class="{'green': selectedName===i}">
          {{i}}
        </v-btn>
      </v-badge>
    </v-layout>

    <div v-if='getRecentDataStream.length>0'>
      <v-layout row>
        <v-text-field label="Gesture Name" solo v-model="saveName" ref='nameField' :rules="[v => !!v || 'Name is required']"></v-text-field>
        <v-btn color="success" @click='saveCapture(saveName)'>Save</v-btn>
        <v-btn color="error" @click='CLEAR_CAPTURE()'>Clear</v-btn>
      </v-layout>
    </div>

    <import-box></import-box>
    <export-box></export-box>

  </v-container>
</template>

<script>
import {mapGetters, mapMutations} from 'vuex'
import LiveDataSheetSuper from './LiveDataSheetSuper.vue'
import ExportBox from './ExportBox.vue'
import ImportBox from './ImportBox.vue'

export default {
  data () {
    return {
      dataStream: [],
      saveName: '',
      selectedName: ''
    }
  },
  computed: {
    ...mapGetters(['getDataAll', 'isCapturing', 'getRecentDataStream', 'getCapturedDataStream'])
  },
  methods: {
    ...mapMutations(['START_CAPTURE', 'STOP_CAPTURE', 'SAVE_CAPTURE', 'CLEAR_CAPTURE', 'REMOVE_CAPTURE', 'RENAME_CAPTURE']),
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
    startCapture () {
      this.dataStream = this.getRecentDataStream
      this.START_CAPTURE()
    },
    stopCapture () {
      this.STOP_CAPTURE()
    },
    saveCapture (name) {
      this.STOP_CAPTURE()
      if (this.$refs.nameField.validate()) {
        this.SAVE_CAPTURE(name)
        global.vm.$forceUpdate()
      }
    },
    rename (oldname) {
      let newname = prompt('Please enter new name:', '')
      if (newname !== null && newname !== '') {
        this.RENAME_CAPTURE({oldname: oldname, newname: newname})
      }
    }
  },
  mounted () {
    // this.dataStream = this.getDataAll
  },
  components: {LiveDataSheetSuper, ExportBox, ImportBox}
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
