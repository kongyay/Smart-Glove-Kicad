<template>
  <v-layout column align-center>
    <v-layout row>
      <v-checkbox label="Acc" v-model="showAcc"></v-checkbox>
      <v-checkbox label="Gyro" v-model="showGyro"></v-checkbox>
      <v-checkbox label="Mag" v-model="showMag"></v-checkbox>
      <v-checkbox label="Flex" v-model="showFlex"></v-checkbox>
    </v-layout>
    <v-layout row v-if='showAcc'>
      <live-data-chart v-for="(value,i) in [0,1,2]" :key='i' :dataset="getDataOne(value)" :minVal="-100" :maxVal="100" :name='getHeadNames[value]' color="#FF0000"></live-data-chart>
    </v-layout>
    <v-layout row v-if='showGyro'>
      <live-data-chart v-for="(value,i) in [3,4,5]" :key='i' :dataset="getDataOne(value)" :minVal="-100" :maxVal="100" :name='getHeadNames[value]' color="#FFFF00"></live-data-chart>
    </v-layout>
    <v-layout row v-if='showMag'>
      <live-data-chart v-for="(value,i) in [6,7,8]" :key='i' :dataset="getDataOne(value)" :minVal="-100" :maxVal="100" :name='getHeadNames[value]' color="#FF00FF"></live-data-chart>
    </v-layout>
    <v-layout row v-if='showFlex'>
      <live-data-chart v-for="(value,i) in [9,10,11]" :key='i' :dataset="getDataOne(value)" :minVal="0" :maxVal="getMaxVals[i]" :name='getHeadNames[value]' color="#00FFFF"></live-data-chart>
    </v-layout>
    <v-layout row v-if='showFlex'>
      <live-data-chart v-for="(value,i) in [12,13]" :key='i' :dataset="getDataOne(value)" :minVal="0" :maxVal="getMaxVals[i]" :name='getHeadNames[value]' color="#00FFFF"></live-data-chart>
    </v-layout>
    <v-layout row v-if='false'>
      <live-data-table :header="getHeadNames.slice(9,14)" :dataset="getDataFlex" :minVal="0" :maxVal="1023"></live-data-table>
      <live-data-table :header="getHeadNames.slice(0,3)" :dataset="getDataAcc" :minVal="-2000"  :maxVal="2000"></live-data-table>
      <live-data-table :header="getHeadNames.slice(3,6)" :dataset="getDataGyro" :minVal="-2000" :maxVal="2000"></live-data-table>
      <live-data-table :header="getHeadNames.slice(6,9)" :dataset="getDataMag" :minVal="-5000" :maxVal="5000"></live-data-table>
    </v-layout>
  </v-layout>

</template>

<script>
import LiveDataTable from './LiveDataTable.vue'
import LiveDataChart from './LiveDataChart.vue'
import { mapGetters } from 'vuex'

export default {
  props: {
    dataStream: Array
  },
  data () {
    return {
      showAcc: false,
      showGyro: false,
      showMag: false,
      showFlex: true
    }
  },
  computed: {
    ...mapGetters(['getHeadNames', 'getMaxVals', 'getQuantized']),
    getDataFlex () {
      return this.dataStream.map((d) => d.slice(9, 14))
    },
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
    getDataOne (col) {
      return this.dataStream.map((d) => d[col])
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
