<template>
  <div>
    <v-expansion-panel  expand>
      <v-expansion-panel-content>
        <div slot="header">Export...</div>
        <v-card>
          <v-card-text class="grey lighten-5">
            <v-layout column justify-center>
              <v-layout row>
                <h4>Include Sensors</h4>
                <v-checkbox v-for='(val,i) in includeSensor' :key=i :label="getHeadNamesIMU[i]" v-model="includeSensor[i]"></v-checkbox>
              </v-layout>
              <v-layout row>
                <h4>Include Axis</h4>
                <v-checkbox v-for='(val,i) in includeAxis' :key=i :label="String(i)" v-model="includeAxis[i]"></v-checkbox>
              </v-layout>
              <v-layout row>
                <h4>Include Gestures</h4>
                <v-btn @click="includeGestures = Object.keys(getCapturedDataStreamIMU)">All</v-btn>
                <v-select
                  v-model="includeGestures"
                  :items="Object.keys(getCapturedDataStreamIMU)"
                  chips
                  multiple
                ></v-select>
              </v-layout>
              <v-layout row>
                <h4>Format</h4>
                <v-radio-group v-model="format">
                  <v-radio label="CSV" value="CSV"></v-radio>
                  <v-radio label="JSON" value="JSON" disabled></v-radio>
                </v-radio-group>
              </v-layout>
              <v-layout row>
                  <v-btn color='success' @click='exportCSV()'>Export</v-btn>
              </v-layout>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  data () {
    return {
      panelOpen: false,
      includeSensor: [true, true, true, true, true, true],
      includeAxis: [true, true, true],
      format: 'CSV',
      includeGestures: []
    }
  },
  computed: {
    ...mapGetters(['getDataAll', 'isCapturing', 'getRecentDataStreamIMU', 'getCapturedDataStreamIMU', 'getHeadNamesIMU'])
  },
  methods: {
    exportCSV () {
      if (this.includeGestures.length === 0) {
        return
      }

      let csvContent = 'data:text/csv;charset=utf-8,'
      // csvContent += (this.includeAcc ? ',accX,accY,accZ' : '') +
      // (this.includeGyro ? ',gyroX,gyroY,gyroZ' : '') +
      // (this.includeMag ? ',magX,magY,magZ' : '') +
      // (this.includeFlex ? ',flex1,flex2,flex3,flex4,flex5' : '') + ',gesture\n'
      for (let gesture of this.includeGestures) {
        for (let row of this.getCapturedDataStreamIMU[gesture]) {
          // row = [[finger],[finger],....]
          for (let i = this.includeSensor.length; i > 0; i--) {
            row = this.includeSensor[i] ? row : row.slice(0, i).concat(row.slice(i + 1))
          }
          for (let i = this.includeAxis.length; i > 0; i--) {
            row = this.includeAxis[i] ? row : row.map(a => this.includeAxis[i] ? a : a.slice(0, i).concat(a.slice(i + 1)))
          }
          row = row.map(r => r.slice(0, 3))
          csvContent += [...[...row], gesture.split('.')[0]].join(',') + '\n'
        }
      }
      console.log(csvContent)
      csvContent = csvContent.slice(0, -1)

      const data = encodeURI(csvContent)
      const link = document.createElement('a')
      link.setAttribute('href', data)
      link.setAttribute('download', 'export.csv')
      link.click()
    }
  },
  watch: {
    'getCapturedDataStreamIMU': {
      handler: function (val, oldVal) {
        // console.log(val)
      },
      deep: true
    }
  }
}
</script>
