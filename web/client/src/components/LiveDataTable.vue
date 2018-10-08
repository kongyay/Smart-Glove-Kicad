<template>
  <v-data-table
      :headers="headers"
      :items="dataset"
      hide-actions
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <td v-for="(value,i) in header" :key='i' class="text-xs-right" :style="`background-color:rgb(${colorCode(props.item[i])},255,255)`">{{ props.item[i] }}</td>
      </template>
  </v-data-table>
</template>

<script>
export default {
  props: {
    header: Array,
    maxVal: Number,
    minVal: Number,
    dataset: Array
  },
  data () {
    return {
      headers: this.header.map((h) => { return {text: h} })
    }
  },
  methods: {
    colorCode (item) {
      return 255 - item / (this.maxVal - this.minVal) * 255
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
td {
  padding: "10px";
}
</style>
