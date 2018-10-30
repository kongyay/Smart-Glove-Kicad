<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <live-data-sheet-all-i-m-u :data-stream='dataStream'></live-data-sheet-all-i-m-u>
    </v-slide-y-transition>

    <v-layout row wrap>
      <v-btn color="secondary" @click='goLive()'>LIVE</v-btn>
      <v-btn color="secondary" @click='goNone()'>NONE</v-btn>
    </v-layout>

  </v-container>
</template>

<script>
import {mapGetters, mapMutations} from 'vuex'
import LiveDataSheetAllIMU from '../LiveDataSheetAllIMU.vue'
import ExportBox from '../ExportBox.vue'
import ImportBox from '../ImportBox.vue'

export default {
  data () {
    return {
      dataStream: []
    }
  },
  computed: {
    ...mapGetters(['getDataAllIMU'])
  },
  methods: {
    ...mapMutations([]),
    goLive () {
      this.dataStream = this.getDataAllIMU
    },
    goNone () {
      this.dataStream = []
    }
  },
  mounted () {
    // this.dataStream = this.getDataAll
  },
  components: {LiveDataSheetAllIMU, ExportBox, ImportBox}
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
