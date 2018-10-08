<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
          <live-data-table :header="['โป้ง', 'ชี้', 'กลาง', 'นาง', 'ก้อย']" :dataset="getDataFlex" :minVal="0" :maxVal="1023"></live-data-table>
          <live-data-table :header="['X','Y','Z']" :dataset="getDataAcc" :minVal="-400"  :maxVal="400"></live-data-table>
          <live-data-table :header="['X','Y','Z']" :dataset="getDataGyro" :minVal="-400" :maxVal="400"></live-data-table>
          <live-data-table :header="['X','Y','Z']" :dataset="getDataMag" :minVal="-5000" :maxVal="5000"></live-data-table>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import {mapGetters} from 'vuex'
import LiveDataTable from './LiveDataTable.vue'
export default {
  data () {
    return {

    }
  },
  computed: {
    ...mapGetters(['getDataFlex', 'getDataAcc', 'getDataGyro', 'getDataMag'])
  },
  components: {LiveDataTable}
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
