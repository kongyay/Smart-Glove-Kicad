<template>
  <line-chart
          :chart-data="chartData"
          :options="chartOption"
          :width="400"
          :height="150"
          >
        </line-chart>
</template>

<script>
import LineChart from '../services/LineChart.js'
export default {
  props: {
    maxVal: Number,
    minVal: Number,
    name: String,
    dataset: Array,
    color: String
  },
  data () {
    return {
      datalabel: 'test-label',
      chartOption: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 0
        },
        scales: {
          yAxes: [{
            ticks: {
              min: this.minVal,
              max: this.maxVal,
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }],
          xAxes: [ {
            gridLines: {
              display: true
            }
          }],
          legend: {
            display: true
          }
        }
      }
    }
  },
  computed: {
    chartData () {
      let labelsTemp = Array.from(Array(this.dataset.length).keys())
      return {
        labels: labelsTemp,
        datasets: [
          {
            label: this.name,
            backgroundColor: this.color,
            data: this.dataset
          }
        ]
      }
    }
  },
  methods: {
    colorCode (item) {
      return 255 - item / (this.maxVal - this.minVal) * 255
    },
    reGraph () {

    }
  },
  mounted () {
    // this.reGraph()
  },
  components: {
    LineChart
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
