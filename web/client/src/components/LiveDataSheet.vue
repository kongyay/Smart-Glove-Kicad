<template>
  <v-layout column align-center justify-space-around>
    <v-layout row justify-space-around>
      <v-checkbox v-for="(x,no) in 6" :key='"cb"+no' :label="getHeadNamesIMU[no]" v-model="show[no]"></v-checkbox>
    </v-layout>
    <div v-for="(x,no) in 6" :key='"ch"+no'>
      <v-layout row wrap v-if='show[no]'>
        <h4>{{getHeadNamesIMU[no]}}</h4>
        <live-data-chart v-for="(axis,x) in 6" :key='x' :dataset="getDataSet(no,x)" :minVal="(axis<3)? -10000:-50" :maxVal="(axis<3)? 10000:50" color="#FF0000"></live-data-chart>
      </v-layout>
      <v-divider></v-divider>
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
    ...mapGetters(['getHeadNamesIMU', 'getIdlePoints'])
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
          label: 'Main' + no,
          backgroundColor: '#FF0000',
          data: this.getDataOne(no, axis),
          pointBackgroundColor: this.getIdlePoints
        },
        {
          label: 'BG' + no,
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
