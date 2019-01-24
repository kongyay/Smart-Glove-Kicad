<template>
  <v-btn block outline color="pink" >
    {{action.name}}
  </v-btn>
</template>

<script>
export default {
  props: {
    action: Object
  },
  data () {
    return {

    }
  },
  computed: {

  },
  methods: {

  },
  components: {

  }
}
</script>

<style scoped>
img {
  width: 50px;
  height: 50px;
}
table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}
table, th, td {
  border: 1px solid black;
}
.white {
  background-color: white;
}
.black {
  background-color: black;
}
</style>
