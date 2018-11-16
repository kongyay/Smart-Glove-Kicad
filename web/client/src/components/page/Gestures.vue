<template>
  <v-container fluid>
    <gesture-box name="Gesture 1"></gesture-box>
    <gesture-box name="Gesture 2"></gesture-box>
  </v-container>
</template>

<script>
import GestureBox from '../GestureBox.vue'
export default {
  components: {
    GestureBox
  }
}
</script>
