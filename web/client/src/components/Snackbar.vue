<template>
  <v-snackbar
    v-model="enabled" bottom right :timeout="3000"
  >
    <v-icon dark
      class="mr-3"
    >
      info
    </v-icon>
    <div>{{ snackbarText }}</div>
    <v-icon medium dark
      @click="enabled = false"
    >
      close
    </v-icon>

  </v-snackbar>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data () {
    return {

    }
  },
  computed: {
    ...mapState({
      snackbarText: state => state.user.snackbarText
    }),
    enabled: {
      get: function () {
        return this.$store.state.user.snackbarEnabled
      },
      set: function (newValue) {
        this.$store.state.user.snackbarEnabled = newValue
      }
    }
  },
  methods: {
  },
  name: 'App'
}
</script>
