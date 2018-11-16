<template>
  <v-layout column align-center>
    <v-layout row>
      <v-checkbox v-for="(x,no) in 6" :key='"cb"+no' :label="x.toString()" v-model="show[no]"></v-checkbox>
    </v-layout>
    <div v-for="(x,no) in 6" :key='"ch"+no'>
      <v-layout row v-if='show[no]'>
        <live-data-chart v-for="(axis,x) in [0,1,2]" :key='x' :dataset="getDataSet(no,axis)" :minVal="(no>0)? -180:-180" :maxVal="(no>0)? 360:360" :name='getHeadNamesIMU[axis]' color="#FF0000"></live-data-chart>
      </v-layout>
      <!-- <v-layout row v-if='show[no]'>
        <live-data-chart v-for="(axis,x) in [3,4,5]" :key='x' :dataset="getDataOne(no,axis)" :minVal="-1000" :maxVal="1000" :name='getHeadNamesIMU[axis]' color="#00FF00"></live-data-chart>
      </v-layout>
      <v-layout row v-if='show[no]'>
        <live-data-chart v-for="(axis,x) in [6,7,8]" :key='x' :dataset="getDataOne(no,axis)" :minVal="-2000" :maxVal="2000" :name='getHeadNamesIMU[axis]' color="#0000FF"></live-data-chart>
      </v-layout> -->
    </div>
  </v-layout>

</template>

<script>
import LiveDataTable from './LiveDataTable.vue'
import LiveDataChart from './LiveDataChart.vue'
import { mapGetters } from 'vuex'

export default {
  props: {
    dataStream: Array,
    dataBG: Array
  },
  data () {
    return {
      show: [false, false, false, false, false, false]
    }
  },
  computed: {
    ...mapGetters(['getHeadNamesIMU']),
    getDataAcc () {
      return this.dataStream.map((d) => d.slice(0, 3))
    },
    getDataGyro () {
      return this.dataStream.map((d) => d.slice(3, 6))
    },
    getDataMag () {
      return this.dataStream.map((d) => d.slice(6, 9))
    }
  },
  methods: {
    getDataOne (no, axis) {
      return this.dataStream.map((d) => d[no][axis])
    },
    getDataBG (no, axis) {
      return this.dataBG.map((d) => d[no][axis])
    },
    getDataSet (no, axis) {
      return [
        {
          label: 'Main',
          backgroundColor: '#FF0000',
          data: this.getDataOne(no, axis)
        },
        {
          label: 'BG',
          backgroundColor: '#0000FF',
          data: this.getDataBG(no, axis)
        }
      ]
    }
  },
  components: {LiveDataTable, LiveDataChart}
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
</style>
